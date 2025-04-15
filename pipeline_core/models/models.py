import importlib
import logging

import openai

from pipeline_core.utils.utils import load_yaml  # or wherever you keep it

logging.getLogger("promptflow").setLevel(logging.DEBUG)
# OpenAI API Key (⚠️ Replace with secure retrieval method)
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.AsyncOpenAI(api_key=openai.api_key)

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


# PythonBlock


class PythonBlock:
    def __init__(self, config: dict):
        self.id = config["id"]
        self.inputs = config["inputs"]
        self.outputs = config["outputs"]
        self.script = config.get("script")
        self.code = config.get("code")
        self.params = config.get("params", {})

    def run(self, context: dict) -> dict:
        input_values = {k: context[k] for k in self.inputs}

        if self.script:
            module_path, func_name = self.script.rsplit(".", 1)
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            result = func(input_values, **self.params)

        elif self.code:
            local_vars = {"inputs": input_values}
            exec(self.code, {}, local_vars)
            result = local_vars.get("result") or next(iter(local_vars.values()))
        else:
            raise ValueError("PythonBlock requires either 'script' or 'code'.")

        if not isinstance(result, dict):
            result = {self.outputs[0]: result}

        return result


# models/models.py

import json
import os
from pathlib import Path

# import prompty


openai.api_type = os.getenv("OPENAI_API_TYPE", "openai")  # prevents ambiguity errors

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from promptflow.core import Prompty

# os.environ["OPENAI_API_TYPE"] = "openai"

# os.getenv("OPENAI_BASE_URL")


class PromptBlock:
    def __init__(self, config):
        self.id = config["id"]
        self.inputs = config.get("inputs", [])
        self.outputs = config.get("outputs", [self.id])
        self.executor = ThreadPoolExecutor()  # Add this line for reuse

        # Resolve prompty path relative to project root
        base_dir = Path(__file__).resolve().parents[1]
        self.prompty_path = base_dir / "prompts" / f"{self.id}.prompty"

        # Optional: show in dev mode
        if os.getenv("PROMPTFLOW_DEBUG"):
            print(f"📄 Loading prompty: {self.prompty_path}")

        # Load model config override from env
        self.model_override = {
            "api": "chat",
            "configuration": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                # "base_url": os.getenv("OPENAI_BASE_URL"),  # Optional
                "model": "gpt-3.5-turbo",
            },
            "parameters": {
                "temperature": float(os.getenv("PROMPT_TEMP", "0.3")),
                "max_tokens": int(os.getenv("PROMPT_MAX_TOKENS", "512")),
            },
        }

        # Load the prompty object
        # self.prompty = Prompty.load(source=str(self.prompty_path))

        # print("🌐 ENV OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
        # print("🌐 ENV OPENAI_BASE_URL:", os.getenv("OPENAI_BASE_URL"))
        # import socket
        # print("🌐 CAN RESOLVE openai.com:", socket.gethostbyname("api.openai.com"))

        self.prompty = Prompty.load(
            source=str(self.prompty_path), model=self.model_override
        )

    # import json

    @staticmethod
    def _maybe_parse_json_string(value):
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, (list, dict)):
                    return parsed
            except json.JSONDecodeError:
                pass
        return value

    async def run(self, context: dict) -> dict:
        try:
            # input_values = {k: context[k] for k in self.inputs}
            input_values = {
                k: self._maybe_parse_json_string(context[k]) for k in self.inputs
            }
            print(os.getenv("PROMPTFLOW_PREVIEW"))

            if os.getenv("PROMPTFLOW_PREVIEW"):
                for k, v in input_values.items():
                    if isinstance(context[k], str) and isinstance(v, (dict, list)):
                        print(
                            f"🧹 Auto-parsed stringified input for '{k}': now {type(v)}"
                        )

            if os.getenv("PROMPTFLOW_PREVIEW"):
                print(f"\n🔍 [DEBUG] Block ID: {self.id}")
                print(f"📄 Prompty path: {self.prompty_path}")
                print(f"📥 Inputs: {input_values}")
                print(f"⚙️  Model override: {self.model_override}")
                print(f"🚀 Calling Prompty...")

            if os.getenv("PROMPTFLOW_PREVIEW"):
                try:
                    rendered = self.prompty.render(**input_values)
                    print("🧪 Rendered Prompt:\n", rendered)
                except Exception as preview_err:
                    print(f"⚠️  Could not render prompt preview: {preview_err}")

            # Run in a background thread to avoid blocking FastAPI event loop
            try:

                prompt = self.prompty.render(**input_values)

                response = openai.chat.completions.create(
                    model=self.model_override["configuration"]["model"],
                    messages=(
                        prompt
                        if isinstance(prompt, list)
                        else [{"role": "user", "content": prompt}]
                    ),
                    temperature=self.model_override["parameters"]["temperature"],
                    max_tokens=self.model_override["parameters"]["max_tokens"],
                )
                result = response.choices[0].message.content.strip()
            except Exception as e:
                import traceback

                traceback.print_exc()
                print(f"🔴 Full Exception: {repr(e)}")
                raise

            if isinstance(result, dict):
                return result
            return {self.outputs[0]: result}

        except Exception as e:
            print(f"❌ Error running prompt '{self.id}': {repr(e)}")
            raise


# class PromptCard:
#     def __init__(self, config: dict):
#         self.id = config.get("id")
#         self.system = config["system"]
#         self.user_template = config["user"]
#         self.model = config.get("model", "gpt-4")
#         self.schema = config.get("schema", None)
#         self.function_name = config.get("function_name", None)
#         self.outputs = config.get("outputs", [self.id])

#     def format_prompt(self, context: dict):
#         return [
#             {"role": "system", "content": self.system},
#             {"role": "user", "content": self.user_template.format(**context)}
#         ]

#     async def run(self, context: dict) -> dict:
#         import openai
#         client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

#         messages = self.format_prompt(context)

#         response = await client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             temperature=0.3
#         )

#         output_text = response.choices[0].message.content.strip()

#         # 👇 This is the key line — store under the declared output key
#         return {self.outputs[0]: output_text}


import inspect


class PromptFlowRunner:
    def __init__(self, flow_config: dict):  # ✅ expects dict now
        self.flow_config = flow_config
        self.blocks = [build_block(cfg) for cfg in self.flow_config["steps"]]

    async def run(self, initial_input):
        data = initial_input
        for block in self.blocks:
            print(f"▶️ Running block: {block.id}")
            if inspect.iscoroutinefunction(block.run):
                data = await block.run(data)
            else:
                data = block.run(data)  ##########
        return data


#     runner = PromptFlowRunner(flow_config)
# await runner.run(initial_input)


# def build_block(step_config: dict):
#     if step_config["type"] == "prompt":
#         return PromptCard(step_config)
#     elif step_config["type"] == "python":
#         return PythonBlock(step_config)
#     else:
#         raise ValueError(f"Unsupported block type: {step_config['type']}")


def build_block(step_config: dict):
    if step_config["type"] == "prompt":
        return PromptBlock(step_config)  # 👈 use PromptyTool-based block
    elif step_config["type"] == "python":
        return PythonBlock(step_config)
    else:
        raise ValueError(f"Unsupported block type: {step_config['type']}")
