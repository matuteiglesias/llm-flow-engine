# flow_api.py
from typing import List, Optional

from core_ai.execution.runner import run_prompt_block
from core_ai.flows.loader import load_prompt_config
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class FlowRequest(BaseModel):
    text: Optional[str] = Field(None)
    path: Optional[str] = Field(None)


class RunBatchRequest(BaseModel):
    files: List[str]
    flow_name: str
    prompt: Optional[str] = None
    model: Optional[str] = "gpt-4o-mini"


@router.post("/{flow_name}")
async def run_named_flow(flow_name: str, req: FlowRequest):
    config = load_prompt_config(flow_name)
    content = req.text or (open(req.path).read() if req.path else "")
    return await run_prompt_block(config, content)


@router.post("/run_batch_flow")
async def run_batch_flow(req: RunBatchRequest):
    results = []
    for path in req.files:
        config = load_prompt_config(req.flow_name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        result = await run_prompt_block(config, content)
        results.append(result)
    return {"results": results}
