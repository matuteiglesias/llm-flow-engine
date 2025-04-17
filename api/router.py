# api/router.py

import asyncio
import uuid
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from pipeline_core.models.models import PromptFlowRunner, build_block
from pipeline_core.utils.utils import load_flow_inputs, load_yaml

# ✅ This is your root router, mounted as /api in main.py
router = APIRouter(prefix="/api")  # ← THIS IS KEY

# ----------------------------
# 🧠 API Input Models
# ----------------------------

class FlowInput(BaseModel):
    flow_path: str
    input_data: dict = {}

class BlockInput(BaseModel):
    block_config: dict
    context: dict = {}

# ----------------------------
# ▶️ Run a full flow
# ----------------------------
@router.post("/run_flow")
async def run_flow(payload: FlowInput):
    # try:
    flow_config = load_yaml(payload.flow_path)

    # Default input fallback
    if not payload.input_data or not payload.input_data.get("text_input"):
        payload.input_data = load_flow_inputs(flow_config)

    run_id = str(uuid.uuid4())
    runner = PromptFlowRunner(flow_config)
    output = await runner.run(payload.input_data, run_id=run_id)

    return {"output": output, "run_id": run_id}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# ▶️ Run a single block
# ----------------------------
@router.post("/run_block")
async def run_block(payload: BlockInput):
    try:
        block = build_block(payload.block_config)
        if asyncio.iscoroutinefunction(block.run):
            result = await block.run(payload.context)
        else:
            result = block.run(payload.context)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# 🧪 Test OpenAI Connection
# ----------------------------
import openai

@router.get("/test_openai")
async def test_openai_connect():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        res = openai.Model.list()
        return {"success": True, "models": [m.id for m in res.data]}
    except Exception as e:
        return {"success": False, "error": str(e)}
