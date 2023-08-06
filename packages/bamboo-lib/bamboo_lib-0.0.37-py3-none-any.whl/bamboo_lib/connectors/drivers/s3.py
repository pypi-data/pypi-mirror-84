import os
import hashlib
import tempfile
import boto3
from botocore.exceptions import ClientError
import progressbar

from bamboo_lib.logger import logger
from bamboo_lib.connectors.models import BaseDriver
from bamboo_lib.helpers import decrypt, process_uri_wildcards, wildcard_matches
from bamboo_lib.exceptions import InvalidCredentialsException

from urllib.parse import urlparse

class S3Driver(BaseDriver):
    TYPE = 'AWS S3 Cloud Storage Driver'

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
            force=None,
            region_name=None,
            delimiter="/",
            **kwargs):
        self.timeout = kwargs.get("timeout", None)
        self.force = force
        self.delimiter = delimiter
        super().__init__(**kwargs)
        self._client = boto3.client('s3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def serialize(self):
        return {
            "timeout": self.timeout,
            "force": self.force,
            "delimiter": self.delimiter,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "region_name": self.region_name,
            "driver": "s3",
        }

    @classmethod
    def deserialize(cls, kwargs):
        return cls(**kwargs)


    def get_matching_s3_objects(self, bucket, prefix="", suffix=""):
        """
        Generate objects in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch objects whose key starts with
            this prefix (optional).
        :param suffix: Only fetch objects whose keys end with
            this suffix (optional).
        """
        paginator = self._client.get_paginator("list_objects_v2")

        kwargs = {'Bucket': bucket}

        # We can pass the prefix directly to the S3 API.  If the user has passed
        # a tuple or list of prefixes, we go through them one by one.
        if isinstance(prefix, str):
            prefixes = (prefix, )
        else:
            prefixes = prefix

        for key_prefix in prefixes:
            kwargs["Prefix"] = key_prefix

            for page in paginator.paginate(**kwargs):
                try:
                    contents = page["Contents"]
                except KeyError:
                    break

                for obj in contents:
                    key = obj["Key"]
                    if key.endswith(suffix):
                        yield obj


    def list_blobs(self, bucket, prefix="", suffix=""):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        try:
            for obj in self.get_matching_s3_objects(bucket, prefix, suffix):
                yield obj["Key"]
        except ClientError as e:
            raise ValueError("Could not build client paginator. Confirm you have correct permissions? (Original Error: {})".format(e))


    @staticmethod
    def uri_to_components(aws_uri_str):
        parsed_info = urlparse(aws_uri_str)
        bucket_name = parsed_info.netloc
        path = parsed_info.path[1:] if parsed_info.path and parsed_info.path.startswith("/") else parsed_info.path
        return bucket_name, path

    def download(self, params=None, **kwargs):
        uri = BaseDriver.resolve_params(self.uri, {"params": params, **kwargs})
        return self.download_single(uri, **kwargs)


    def download_single(self, uri, params=None, http_params=None, force=False, callback=None):
        """Downloads a blob from an S3 bucket."""
        bucket_name, source_path = self.uri_to_components(uri)
        download_path = S3Driver.get_download_path()
        local_filename = os.path.join(download_path, hashlib.sha224(uri.encode("utf-8")).hexdigest())
        logger.info("Downloading AWS resource: {} ...".format(uri))
        # if already downloaded, dont re-download unless required
        if not force and not self.force and os.path.isfile(local_filename):
            logger.info("Reading web asset from local cache...")
            return local_filename
        file_size = self._client.head_object(Bucket=bucket_name, Key=source_path).get('ContentLength')
        logger.info("TARGET FILE ({}) SIZE IS: {} bytes ({} mb)".format(source_path, file_size, round(file_size/1024./1024., 2)))
        # raise ValueError("HERE!!", file_size)

        dl_progress = progressbar.progressbar.ProgressBar(maxval=file_size)
        dl_progress.start()

        def download_progress(chunk):
            dl_progress.update(dl_progress.currval + chunk)

        # raise ValueError(bucket_name, source_path)
        with open(local_filename, 'wb') as f:
            self._client.download_fileobj(bucket_name, source_path, f, Callback=download_progress)

        dl_progress.finish()

        logger.info('Blob {} downloaded to {}.'.format(
            source_path,
            local_filename))
        return local_filename

    @staticmethod
    def aws_uri(bucket, blob_name):
        return "s3://{}/{}".format(bucket, blob_name)

    def get_targets(self, params=None):
        uri = BaseDriver.resolve_params(self.uri, params)
        bucket_name, _ = self.uri_to_components(uri)
        blobs = self.list_blobs(bucket_name)
        blob_strs = [self.aws_uri(bucket_name, obj_path) for obj_path in blobs]
        uri_pattern = process_uri_wildcards(uri)
        results = []
        for uri_to_test in blob_strs:
            matches = wildcard_matches(uri_pattern, uri_to_test)
            if matches:
                results.append((uri_to_test, matches))
        return results

