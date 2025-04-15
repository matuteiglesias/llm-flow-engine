# flow_ui.py
import os
import tempfile
from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile

from pipeline_core.execution.runner import process_files_for_flow

router = APIRouter()


@router.post("/run-flow/")
async def run_named_flow(
    flow_name: str = Form(...),
    user_prompt: Optional[str] = Form(""),
    model: Optional[str] = Form("gpt-4o-mini"),
    files: List[UploadFile] = File(...),
):
    temp_paths = []
    try:
        for f in files:
            path = os.path.join(tempfile.gettempdir(), f.filename)
            with open(path, "wb") as out_file:
                out_file.write(await f.read())
            temp_paths.append(path)

        df = process_files_for_flow(temp_paths, flow_name, user_prompt, model)
        return {"flow": flow_name, "results": df.to_dict(orient="records")}

    finally:
        for path in temp_paths:
            if os.path.exists(path):
                os.remove(path)
