# import asyncio
# import uuid

# import pandas as pd
# from fastapi import FastAPI, File, HTTPException, UploadFile
# from pydantic import BaseModel

# from pipeline_core.ai_blocks.ai_content_generator import *
# from pipeline_core.ai_blocks.file_processor import read_file_content
# from pipeline_core.models.models import PromptFlowRunner
# from pipeline_core.prompts.dispatcher import query_openai
# from pipeline_core.utils.utils import *
# from pipeline_core.utils.utils import load_flow_inputs, load_yaml

# # schema = load_schema("/home/matias/RAG_master/v2/schemas/blog_content_ideas.json")
# # function_name = "blog_content_ideas"


# app = FastAPI()


# # @app.post("/run-flow")
# # async def run_flow(flow_yaml: UploadFile, input_file: UploadFile = None):
# #     # Parse flow
# #     flow_config = load_yaml(await flow_yaml.read())

# #     # Load input (just using 1 text file for now)
# #     input_text = await input_file.read() if input_file else "default input"
# #     initial_input = {"text_input": input_text.decode("utf-8")}

# #     runner = PromptFlowRunner(flow_config)
# #     result = await runner.run(initial_input)

# #     # Save output to file or just return as JSON
# #     run_id = str(uuid.uuid4())
# #     with open(f"outputs/{run_id}.json", "w") as f:
# #         f.write(str(result))

# #     return {"run_id": run_id, "result": result}


# class ExtractionRequest(BaseModel):
#     file_paths: list


# # @app.post("/extract_blog_ideas")
# # async def extract_blog_ideas(request: ExtractionRequest):
# #     try:
# #         # Load your dataframe (assuming df_files is already loaded)
# #         df_files = pd.DataFrame({"FilePath": request.file_paths})

# #         # Function to read file content (reusing logic)
# #         df_files["text"] = df_files["FilePath"].apply(read_file_content)
# #         df_files = df_files.dropna(subset=["text"])

# #         # Get list of document texts
# #         snippets = df_files["text"].tolist()

# #         # Run Async AI Extraction
# #         parsed_docs = await query_openai(
# #             snippets, ai_extract_data, schema=schema, function_name=function_name
# #         )

# #         # Extract structured content into a new column
# #         df_files["parsed_content"] = [
# #             doc["parsed_content"] if "parsed_content" in doc else ""
# #             for doc in parsed_docs
# #         ]

# #         # Sort by Datetime
# #         df_files = df_files.sort_values("Datetime")

# #         return df_files[["FilePath", "parsed_content"]].to_dict(orient="records")
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))
