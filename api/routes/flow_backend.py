# api/routes/flow_backend.py

import os
import json
import logging
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from pipeline_core.utils.utils import read_file_as_text

# -----------------------------------------------------------------------------
# 📁 Constants and Router Setup
# -----------------------------------------------------------------------------

router = APIRouter()
RUNS_DIR = Path(".runs")
BASE_YAML_DIR = Path("pipeline_core/flows").resolve()

# -----------------------------------------------------------------------------
# 📦 Utility: Create Folder for New Run
# -----------------------------------------------------------------------------

def init_run_folder(run_id: str) -> Path:
    run_folder = RUNS_DIR / run_id
    run_folder.mkdir(parents=True, exist_ok=True)
    return run_folder

# -----------------------------------------------------------------------------
# 🧠 Model: Batch Flow Execution
# -----------------------------------------------------------------------------

class FlowRequest(BaseModel):
    text: Optional[str] = Field(None)
    path: Optional[str] = Field(None)
    run_id: Optional[str] = None

class RunBatchRequest(BaseModel):
    files: List[str]
    flow_name: str
    run_id: Optional[str] = None
    prompt: Optional[str] = None
    model: Optional[str] = "gpt-4o-mini"
    resume_from: Optional[bool] = False  # ✅ for 14️⃣

# -----------------------------------------------------------------------------
# 🧩 Load Prompt Config (Not yet used)
# -----------------------------------------------------------------------------

def load_prompt_config(flow_name: str) -> dict:
    path = os.path.join(os.path.dirname(__file__), f"{flow_name}.json")
    with open(path, "r") as f:
        return json.load(f)

# -----------------------------------------------------------------------------
# 💾 Save YAML File
# -----------------------------------------------------------------------------

class SaveYamlRequest(BaseModel):
    path: str
    content: str

@router.post("/save_yaml")
def save_yaml(data: SaveYamlRequest):
    try:
        with open(data.path, "w", encoding="utf-8") as f:
            f.write(data.content)
        return {"status": "success", "path": data.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------------------
# 📖 Read YAML File (Flow Config)
# -----------------------------------------------------------------------------

@router.get("/yaml")
def get_yaml_file(path: str = Query(...)):
    try:
        full_path = Path(path).resolve()
        print("🔍 Looking for YAML at:", full_path)

        # 🔒 Optional: limit access to inside flows dir
        if not str(full_path).startswith(str(BASE_YAML_DIR)):
            raise HTTPException(status_code=403, detail="Access outside allowed scope")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        with open(full_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# # api/routes/flow_backend.py
# import uuid
# import os
# import json
# from pathlib import Path
# from fastapi import APIRouter, HTTPException
# from typing import List, Optional

# PROMPT_WRAPPERS = {
#     "code_review": ai_coder_see_script,
#     # "summarize": ai_summarizer,
#     # Add more mappings here
# }

# # # ----- Dispatcher -----
# # async def query_openai(snippets, prompt_wrapper, **kwargs):
# #     tasks = [prompt_wrapper(snippet, **kwargs) for snippet in snippets]
# #     return await asyncio.gather(*tasks)


# async def run_prompt_block(prompt_config: dict, text: str) -> dict:
#     """
#     Run a single prompt block based on a config and input text.
#     """
#     flow = prompt_config.get("flow")
#     user_prompt = prompt_config.get("user_prompt", "")

#     prompt_wrapper = PROMPT_WRAPPERS.get(flow)
#     if not prompt_wrapper:
#         raise ValueError(f"No wrapper registered for flow '{flow}'")

#     result = await query_openai([text], prompt_wrapper, prompt=user_prompt)
#     return result[0] if result else {"error": "No result returned"}


# @router.post("/{flow_name}")
# async def run_named_flow(flow_name: str, req: FlowRequest):
#     try:
#         run_id = req.run_id or str(uuid.uuid4())
#         run_folder = init_run_folder(run_id)

#         config = load_prompt_config(flow_name)
#         content = req.text or (open(req.path).read() if req.path else "")

#         result = await run_prompt_block(config, content)

#         # ✅ Save inputs/outputs
#         (run_folder / "flow.output.json").write_text(json.dumps(result, indent=2))

#         return {"run_id": run_id, "output": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Flow execution failed: {e}")


# @router.post("/run_batch_flow")
# async def run_batch_flow(req: RunBatchRequest):
#     run_id = req.run_id or str(uuid.uuid4())
#     run_folder = init_run_folder(run_id)
#     results = []
#     status_log = []

#     for i, path in enumerate(req.files):
#         try:
#             config = load_prompt_config(req.flow_name)
#             with open(path, "r", encoding="utf-8") as f:
#                 content = f.read()

#             result = await run_prompt_block(config, content)

#             results.append(json.dumps({"line": i, "result": result}))
#             status_log.append(json.dumps({"line": i, "status": "success"}))
#         except Exception as e:
#             status_log.append(json.dumps({"line": i, "status": "error", "error": str(e)}))

#     # ✅ Save results and status
#     (run_folder / "results.jsonl").write_text("\n".join(results))
#     (run_folder / "status.jsonl").write_text("\n".join(status_log))

#     return {"run_id": run_id, "lines_processed": len(req.files)}



# # flow_backend.py
# from typing import List, Optional

# from core_ai.execution.runner import run_prompt_block
# from core_ai.flows.loader import load_prompt_config
# from fastapi import APIRouter
# from pydantic import BaseModel, Field

# router = APIRouter()


# class FlowRequest(BaseModel):
#     text: Optional[str] = Field(None)
#     path: Optional[str] = Field(None)


# class RunBatchRequest(BaseModel):
#     files: List[str]
#     flow_name: str
#     prompt: Optional[str] = None
#     model: Optional[str] = "gpt-4o-mini"


# @router.post("/{flow_name}")
# async def run_named_flow(flow_name: str, req: FlowRequest):
#     config = load_prompt_config(flow_name)
#     content = req.text or (open(req.path).read() if req.path else "")
#     return await run_prompt_block(config, content)


# @router.post("/run_batch_flow")
# async def run_batch_flow(req: RunBatchRequest):
#     results = []
#     for path in req.files:
#         config = load_prompt_config(req.flow_name)
#         with open(path, "r", encoding="utf-8") as f:
#             content = f.read()
#         result = await run_prompt_block(config, content)
#         results.append(result)
#     return {"results": results}
