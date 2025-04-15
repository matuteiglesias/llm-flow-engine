import os

from fastapi import APIRouter

router = APIRouter()

FLOWS_DIR = os.path.join(os.path.dirname(__file__), "../../pipeline_core/flows")

# @router.get("/flow")
# def list_available_flows():
#     files = os.listdir(FLOWS_DIR)
#     flows = [f.replace(".json", "") for f in files if f.endswith(".json")]
#     return {"flows": flows}

import json


def load_prompt_config_f(name: str):
    with open(f"flows/{name}.json") as f:
        return json.load(f)


@router.get("/flow/{flow_name}/schema")
def get_flow_schema(flow_name: str):
    config = load_prompt_config_f(flow_name)
    return config.get("schema", {})
