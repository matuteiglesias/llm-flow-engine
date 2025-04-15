# tests/test_run_hello_flow.py
import pytest

from pipeline_core.models.models import PromptFlowRunner
from pipeline_core.utils.utils import load_yaml


@pytest.mark.asyncio
async def test_run_hello_flow_success():
    flow_path = "pipeline_core/flows/hello.yaml"
    flow_config = load_yaml(flow_path)
    runner = PromptFlowRunner(flow_config)

    output = await runner.run({"text_input": "Hello world"})  # ✅ await it!

    assert isinstance(output, dict)
    assert "file_saved_path" in output
    assert output["file_saved_path"].endswith("translated_back.txt")
