import yaml
from pathlib import Path

def load_manifest(path: str = "pipeline_core/prompts/manifest.yaml") -> dict:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data

def list_prompt_names(manifest: dict):
    return [p["name"] for p in manifest["prompts"]]

def get_prompt_by_name(manifest: dict, name: str):
    for prompt in manifest["prompts"]:
        if prompt["name"] == name:
            return prompt
    return None

# For testing:
if __name__ == "__main__":
    manifest = load_manifest()
    print("Available prompts:", list_prompt_names(manifest))
    print("translate_to_spanish prompt:", get_prompt_by_name(manifest, "translate_to_spanish"))
