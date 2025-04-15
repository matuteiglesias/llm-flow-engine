# utils.py
import os

from fastapi import APIRouter, Query

from pipeline_core.flows.loader import load_prompt_config
from pipeline_core.utils.file_scanner import scan_folder

router = APIRouter()

FLOWS_DIR = os.path.join(os.path.dirname(__file__), "../../core_ai/flows")


@router.get("/flow", summary="List available flows")
def list_available_flows():
    files = os.listdir(FLOWS_DIR)
    flows = [f.replace(".json", "") for f in files if f.endswith(".json")]
    return {"flows": flows}


@router.get("/flow/{flow_name}/schema")
def get_flow_schema(flow_name: str):
    config = load_prompt_config(flow_name)
    return config.get("schema", {})


@router.get("/scan")
def scan_files(
    folder: str = Query(...),
    ext: str = Query(".py,.ipynb"),
    exclude: str = Query("__init__,node_modules"),
):
    extensions = [e.strip() for e in ext.split(",")]
    patterns = [p.strip() for p in exclude.split(",")]
    files = scan_folder(folder, include_ext=extensions, exclude_patterns=patterns)
    return {"count": len(files), "files": files}
