import importlib
import logging
from opentelemetry.trace.status import Status, StatusCode
from pipeline_core.utils.utils import load_yaml  # or wherever you keep it

from promptflow.tracing._trace import enrich_span_with_output
from pipeline_core.utils.utils import write_output, setup_logging

logging.getLogger("promptflow").setLevel(logging.DEBUG)

from dotenv import load_dotenv
load_dotenv()

import os
import openai
# print("API KEY:", os.getenv("OPENAI_API_KEY"))
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))



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


import ast


class PromptBlock:
    def __init__(self, config):
        self.id = config["id"]
        self.inputs = config.get("inputs", [])
        self.outputs = config.get("outputs", [self.id])
        self.executor = ThreadPoolExecutor()

        # 📄 Resolve prompty path relative to project root
        base_dir = Path(__file__).resolve().parents[1]
        self.prompty_path = base_dir / "prompts" / f"{self.id}.prompty"

        # 🧠 💥 THIS is the missing line that caused your error
        self.prompty = Prompty.load(str(self.prompty_path))
        
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

        # self.prompty = Prompty.load(
        #     source=str(self.prompty_path), model=self.model_override
        # )

    # import json

    @staticmethod
    def _extract_clean_output(response):
        """
        Handle GPT output that is either a string or a stringified message list.
        If a message list, extract the *last message content*, regardless of role.
        """
        content = response.choices[0].message.content.strip()
        print("CONTENT:", content)

        try:
            # Try parsing the content as a list of messages
            parsed = ast.literal_eval(content)
            if isinstance(parsed, list) and all("content" in m for m in parsed):
                return parsed[-1]["content"]
        except Exception:
            pass

        # If it's just a plain string
        return content


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

                rendered = self.prompty.render(**input_values)
                print("🧪 Rendered Prompt:\n", rendered)

                response = openai.chat.completions.create(
                    model=self.model_override["configuration"]["model"],
                    messages=(
                        rendered
                        if isinstance(rendered, list)
                        else [{"role": "user", "content": rendered}]
                    ),
                    temperature=self.model_override["parameters"]["temperature"],
                    max_tokens=self.model_override["parameters"]["max_tokens"],
                )
                # result = response.choices[0].message.content.strip()
                result = self._extract_clean_output(response)
                RETURNS = {self.outputs[0]: result}
                print("RETURNS", RETURNS)

                return {self.outputs[0]: result}



            except Exception as e:
                import traceback

                traceback.print_exc()
                print(f"🔴 Full Exception: {repr(e)}")
                raise

            # if isinstance(result, dict):
            #     return result
            return {self.outputs[0]: result}

        except Exception as e:
            print(f"❌ Error running prompt '{self.id}': {repr(e)}")
            raise

import inspect


import os
import json
from pathlib import Path

def write_trace(run_id: str, spans: list, base_dir=".runs"):
    """
    Store spans as a trace.json in .runs/{run_id}/
    """
    run_dir = Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    trace_path = run_dir / "trace.json"
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(spans, f, indent=2)

    print(f"📄 Trace written to {trace_path}")


from opentelemetry import trace as otel_trace
from promptflow.tracing._tracer import TraceType
from promptflow.tracing._trace import start_as_current_span
from opentelemetry.trace import SpanKind, Status, StatusCode
from promptflow.tracing import start_trace, trace
import inspect, uuid

from promptflow.tracing._trace import start_as_current_span
from opentelemetry import trace as otel_trace


import json

def safe_json(obj):
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)
        
class PromptFlowRunner:
    def __init__(self, flow_config: dict):
        self.flow_config = flow_config
        self.blocks = [build_block(cfg) for cfg in self.flow_config["steps"]]


    # async def run(self, initial_input, run_id=None):
    #     run_id = run_id or str(uuid.uuid4())


    async def run(self, initial_input, run_id=None):
        run_id = run_id or str(uuid.uuid4())
        setup_logging(run_id)
        start_trace(collection=run_id)
        data = initial_input
        otel_tracer = otel_trace.get_tracer("promptflow")

        for block in self.blocks:
            logging.info(f"▶️ Running block: {block.id}")
            # with trace(name=block.id) as span:
            # from promptflow.tracing import start_as_current_span


            otel_tracer = otel_trace.get_tracer("promptflow")

            with start_as_current_span(otel_tracer, block.id) as span:
                span.set_attribute("kind", "LLM")  # instead of integer 1
                span.set_attribute("block_id", block.id)


                input_values = {k: data.get(k) for k in block.inputs} if hasattr(block, "inputs") else {}


                try:
                    result = await block.run(data) if inspect.iscoroutinefunction(block.run) else block.run(data)
                except Exception as e:
                    logging.error(f"❌ Error in block {block.id}: {e}")
                    raise


                # if inspect.iscoroutinefunction(block.run):
                #     result = await block.run(data)
                # else:
                #     result = block.run(data)

                span.set_attribute("inputs", safe_json(input_values))
                span.set_attribute("outputs", safe_json(result))

                enrich_span_with_output(span, result)
                # spans.append(span.to_dict())
                data = result

        write_output(run_id, data)
        # Save trace
        # write_trace(run_id, spans)
        return data

    from promptflow.tracing._trace import start_as_current_span



    async def run_block_with_trace(block, context):
        span_name = block.id
        tracer = otel_trace.get_tracer("promptflow")

        with start_as_current_span(tracer, span_name) as span:
            try:
                # Record inputs
                span.set_attribute("inputs", context)

                if inspect.iscoroutinefunction(block.run):
                    result = await block.run(context)
                else:
                    result = block.run(context)

                # Record outputs
                span.set_attribute("outputs", result)
                return result

            except Exception as e:
                span.record_exception(e)
                span.set_status(StatusCode.ERROR)
                raise
            

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
