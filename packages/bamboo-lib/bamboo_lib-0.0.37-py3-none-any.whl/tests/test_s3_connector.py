import pytest
import pandas as pd
import os
from bamboo_lib.models import PipelineStep, AdvancedPipelineExecutor
from bamboo_lib.helpers import grab_connector
from bamboo_lib.steps import WildcardDownloadStep, DownloadStep


class ProcessStep(PipelineStep):
    def run_step(self, prev_result, params):
        df = pd.read_csv(prev_result)
        return df



@pytest.fixture()
def s3_pipeline():
    source_connector = grab_connector(__file__, "aws-sg-simple")
    http_dl_step = DownloadStep(connector=source_connector, force=True)
    process_step = ProcessStep()
    pp = AdvancedPipelineExecutor({})
    pp = pp.next(http_dl_step).next(process_step)
    return pp


def test_s3_dl(s3_pipeline):
    res = s3_pipeline.run_pipeline()
    assert res is not None
    assert len(res) == 2
