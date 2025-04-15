# tests/test_promptblock.py
from unittest.mock import MagicMock, patch

import pytest

from pipeline_core.models.models import PromptBlock


@pytest.fixture
def mock_prompty():
    class FakePrompty:
        def __call__(self, **kwargs):
            return "Hola mundo!"

        def render(self, **kwargs):
            return "Rendered prompt"

    return FakePrompty()


class FakePrompty:
    def __call__(self, **kwargs):
        return "Hola mundo!"

    def render(self, **kwargs):
        return "Rendered prompt"


@pytest.mark.asyncio
async def test_promptblock_returns_string():
    config = {
        "id": "test_block",
        "inputs": ["text_input"],
        "outputs": ["translated"],
        # "prompty_path": "pipeline_core/prompts/test_block.prompty",  # add fake .prompty!
    }

    class FakePrompty:
        def render(self, **kwargs):
            return "Rendered prompt"

        def __call__(self, **kwargs):
            return "Hola mundo!"

    with patch("pipeline_core.models.models.Prompty.load", return_value=FakePrompty()):
        block = PromptBlock(config)
        context = {"text_input": "Hello world"}
        result = await block.run(context)
        assert result == {"translated": "Hola mundo!"}


@pytest.mark.asyncio
async def test_promptblock_returns_dict():
    class DictPrompty:
        def __call__(self, **kwargs):
            return {"translated": "Hola mundo!"}

        def render(self, **kwargs):
            return "Rendered prompt"

    config = {"id": "test_block", "inputs": ["text_input"], "outputs": ["translated"]}
    with patch("pipeline_core.models.models.Prompty.load", return_value=DictPrompty()):
        block = PromptBlock(config)
        context = {"text_input": "Hello world"}
        result = await block.run(context)
        assert result == {"translated": "Hola mundo!"}


@pytest.mark.asyncio
async def test_promptblock_raises_exception():
    config = {
        "id": "test_block",
        "inputs": ["text_input"],
        "outputs": ["translated"],
        # "prompty_path": "pipeline_core/prompts/test_block.prompty",
    }

    class FailingPrompty:
        def render(self, **kwargs):
            return "Rendered prompt"

        def __call__(self, **kwargs):
            raise ValueError("Boom")

    with patch(
        "pipeline_core.models.models.Prompty.load", return_value=FailingPrompty()
    ):
        block = PromptBlock(config)
        context = {"text_input": "Hello world"}
        with pytest.raises(ValueError):
            await block.run(context)
