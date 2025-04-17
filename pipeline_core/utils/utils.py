import logging
from datetime import datetime
from pathlib import Path

import yaml
from langchain.text_splitter import RecursiveCharacterTextSplitter

# def save_json(file_path: str, data: dict):
#     """Save a dictionary to a JSON file as a list of entries."""
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     try:
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(list(data.values()), f, indent=4)
#         logging.info(f"✅ json saved to {file_path}.")
#     except Exception as e:
#         logging.error(f"❌ Failed to save json to {file_path}: {e}")


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_text_splitter(file_type, chunk_size=8000, chunk_overlap=100):
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )


def load_flow_inputs(flow_config: dict) -> dict:
    resolved = {}
    for inp in flow_config.get("inputs", []):
        if inp["type"] == "file":
            with open(inp["path"], "r") as f:
                resolved[inp["id"]] = f.read()
    return resolved


# def save_metadata(file_path, data):
#     """Saves metadata to a JSON file."""
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)

#     try:
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=4)
#         logging.info(f"✅ Metadata saved to {file_path}.")
#     except Exception as e:
#         logging.error(f"❌ Failed to save metadata to {file_path}: {e}")

# pipeline_core/utils/io.py

import os


def save_text_to_file(inputs: dict, output_path: str) -> str:
    """
    Save the first value in `inputs` to a text file.

    Args:
        inputs (dict): Dictionary with one or more input values (typically from context).
        output_path (str): Where to save the resulting file.

    Returns:
        str: Path to the saved file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Extract the first (and usually only) input
    content = next(iter(inputs.values()))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"💾 Saved output to {output_path}")
    return output_path


import functools
import json

from openai._base_client import SyncAPIClient


def patch_openai_logging():
    original_request = SyncAPIClient._request

    @functools.wraps(original_request)
    def patched_request(self, *args, **kwargs):
        try:
            request = self._build_request(
                kwargs["options"], retries_taken=kwargs.get("retries_taken", 0)
            )
            self._prepare_request(request)

            print("\n🔎 Final Request Info:")
            print("🔗 URL:", request.url)
            print("📄 METHOD:", request.method)
            print("📦 HEADERS:", dict(request.headers))
            print("📤 BODY:", request.content.decode("utf-8"))
        except Exception as e:
            print(f"[DEBUG PATCH ERROR] Couldn't inspect request: {e}")

        return original_request(self, *args, **kwargs)

    SyncAPIClient._request = patched_request




import json
import logging
import os
from pathlib import Path


def write_output(run_id: str, output: dict, base_dir=".runs"):
    run_dir = Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / "flow.output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"✅ Output written to {out_path}")


def setup_logging(run_id: str, base_dir=".runs", level=logging.INFO):
    run_dir = Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "flow.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

    logging.info(f"📄 Log file initialized at {log_path}")


def read_file_as_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# def scan_folder(base_path, include_ext=None, exclude_patterns=None):
#     base = Path(base_path).expanduser()
#     files = list(base.rglob("*"))

#     def is_valid(f):
#         return (
#             f.is_file()
#             and (not include_ext or f.suffix in include_ext)
#             and all(p not in f.name for p in (exclude_patterns or []))
#         )

#     def file_info(f: Path):
#         stat = f.stat()
#         return {
#             "id": f"{f.stem}_{stat.st_mtime_ns}",  # crude UID
#             "name": f.name,
#             "path": str(f),
#             "ext": f.suffix,
#             "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
#         }

#     return [file_info(f) for f in files if is_valid(f)]


# import os
# import json

# def load_json(file_path: str) -> dict:
#     """Load JSON file into a dictionary, indexing by chunk 'id'."""
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             try:
#                 data = json.load(f)

#                 # ✅ Convert from list to dictionary using `id` as the key
#                 if isinstance(data, list):
#                     print("⚠️ Warning: Metadata stored as a list, converting to dictionary using 'id'.")
#                     return {entry["id"]: entry for entry in data if "id" in entry}

#                 return data  # Already a dictionary
#             except json.JSONDecodeError:
#                 print(f"⚠️ Warning: JSON file {file_path} is corrupted. Resetting.")
#                 return {}

#     return {}  # Return empty dictionary if file does not exist


# def load_schema(file_path):
#     """Loads a JSON schema from a file."""
#     with open(file_path, "r") as file:
#         return json.load(file)


# import yaml

# def load_config(config_path: str) -> dict:
#     """Loads a configuration file from the specified path."""
#     with open(config_path, "r") as file:
#         config = yaml.safe_load(file)
#     return config


# import pandas as pd

# def clean_data(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Cleans the DataFrame by removing empty rows and duplicates.

#     Args:
#         df (pd.DataFrame): The DataFrame to clean.

#     Returns:
#         pd.DataFrame: The cleaned DataFrame.
#     """
#     df = df.dropna(how='all')  # Drop empty rows
#     df = df.drop_duplicates()  # Remove duplicates
#     return df


# import numpy as np
# from sentence_transformers import SentenceTransformer

# # Load pre-trained sentence transformer
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def embed_texts(texts):
#     """Embed a list of texts into numerical vectors using a pre-trained model."""
#     embeddings = np.array([model.encode(text) for text in texts])
#     return embeddings.astype("float32")


# import pandas as pd
# import subprocess
# from pathlib import Path


# def get_recent_files(
#     root="/home/matias/RAG_master/v2",
#     exclude_patterns=None,
#     allowed_extensions=None
# ):
#     if exclude_patterns is None:
#         exclude_patterns = ["__init__.py", "kohya", "ChatDev", "checkpoints", "node_modules"]
#     if allowed_extensions is None:
#         allowed_extensions = [".py", ".ipynb"]

#     # 🧨 Execute bash command
#     cmd = f"find {root} -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n'"
#     output = subprocess.check_output(cmd, shell=True, text=True)

#     # ✅ Parse using regex
#     raw_lines = output.strip().split("\n")
#     df = pd.DataFrame(raw_lines, columns=["raw"])
#     df[["Date", "Time", "FilePath"]] = df["raw"].str.extract(r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s+(.*)$")
#     df.drop(columns=["raw"], inplace=True)

#     # ✅ Timestamps
#     df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')
#     df.drop(columns=["Date", "Time"], inplace=True)
#     df["Year-Month"] = df["Datetime"].dt.strftime('%Y-%m')

#     # ✅ Filters
#     for pattern in exclude_patterns:
#         df = df[~df["FilePath"].str.contains(pattern)]

#     df = df[df["FilePath"].str.endswith(tuple(allowed_extensions))]
#     df = df.dropna(subset=["Datetime"]).drop_duplicates(subset=["FilePath"])
#     df = df.sort_values("Datetime", ascending=False).reset_index(drop=True)

#     return df


# import json

# def safe_json_loads(text: str) -> dict:
#     """Safely parses JSON-like strings, handling errors gracefully."""
#     try:
#         # Convert single quotes to double quotes for valid JSON
#         fixed_text = text.replace("'", '"')
#         return json.loads(fixed_text) if fixed_text.strip().startswith("{") else None
#     except json.JSONDecodeError:
#         return None


# import uuid
# from datetime import datetime
# from pathlib import Path


# import hashlib

# def compute_md5(file_path, block_size=65536):
#     """
#     Computes the MD5 hash of the file located at file_path.
#     Reads the file in binary mode in chunks to handle large files efficiently.
#     """
#     md5 = hashlib.md5()
#     with open(file_path, "rb") as f:
#         for chunk in iter(lambda: f.read(block_size), b""):
#             md5.update(chunk)
#     return md5.hexdigest()

# def file_has_changed(file, stored_file_meta):
#     """
#     Returns True if the current MD5 hash of the file differs from the stored hash,
#     meaning the file has changed; otherwise, returns False.
#     This function avoids heavy metadata extraction and only computes the MD5 checksum.
#     """
#     current_md5 = compute_md5(file)
#     return current_md5 != stored_file_meta.get("hash_md5")


# from typing import Dict, Any
# import magic

# def extract_basic_metadata(file_path: Path) -> Dict[str, Any]:
#     """Extract metadata from a given file, including size, timestamps, and hashes."""
#     if not file_path.is_file():  # ✅ Skip directories
#         raise IsADirectoryError(f"Skipping directory: {file_path}")

#     stat = file_path.stat()

#     file_type = magic.from_file(str(file_path), mime=True)

#     hash_md5 = hashlib.md5(str(file_path).encode()).hexdigest()

#     return {
#         "file_name": file_path.name,
#         "original_path": str(file_path),
#         "file_type": file_type,
#         "size_kb": round(stat.st_size / 1024, 2),
#         "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
#         "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
#         "accessed_at": datetime.fromtimestamp(stat.st_atime).isoformat(),
#         "hash_md5": hash_md5,
#     }


# def create_chunk_metadata(file_id, file_path, chunk_text, chunk_index, chunks_dir):
#     """
#     Creates a chunk metadata record and writes the chunk text to a file.

#     Returns the chunk metadata dictionary or None if an error occurs.
#     """
#     chunk_id = str(uuid.uuid4())
#     chunk_file_path = os.path.join(chunks_dir, f"{chunk_id}.txt")

#     try:
#         with open(chunk_file_path, "w", encoding="utf-8") as chunk_file:
#             chunk_file.write(chunk_text)
#     except Exception as e:
#         logging.error(f"❌ Failed to save chunk {chunk_id} for {file_path}: {e}")
#         print(f"❌ ERROR: Failed to save chunk {chunk_id} for {file_path}: {e}")
#         return None

#     metadata = {
#         "id": chunk_id,
#         "file_id": file_id,
#         "chunk_index": chunk_index,
#         "chunk_file": chunk_file_path,
#         "original_path": file_path,
#         "chunk_size": len(chunk_text),
#         "chunk_words": len(chunk_text.split()),
#         "created_at": datetime.now().isoformat(),
#         "updated_at": datetime.now().isoformat()
#     }
#     return metadata


# def create_file_metadata(file):
#     """
#     Creates metadata for a new file. Returns a tuple:
#     (index_entry, file_meta)
#     where:
#     - index_entry is used in self.file_index keyed by the original path.
#     - file_meta is stored in self.files_metadata keyed by file_id.
#     """
#     metadata = extract_basic_metadata(Path(file))
#     # Generate a new file_id for this file.
#     file_id = str(uuid.uuid4())


# # Extract the file's text content.
# extracted_text = extract_text(file, limit = 1000)

# # Build the index entry for fast lookup.
# file_meta = {
#     "id": file_id,
#     "file_name": metadata["file_name"],
#     "original_path": metadata["original_path"],
#     "file_type": metadata["file_type"],
#     "size_kb": metadata["size_kb"],
#     "created_at": metadata["created_at"],
#     "modified_at": metadata["modified_at"],
#     "accessed_at": metadata["accessed_at"],
#     "extracted_text": extracted_text,
#     "upload_date": datetime.now().isoformat(),
#     "hash_md5": metadata["hash_md5"]
# }

# return file_meta


# def update_file_metadata(file, stored_file_meta):
#     """
#     Updates metadata for an existing file (one that has changed).
#     Uses the existing file_id from stored_file_meta.
#     Returns a tuple: (index_entry, file_meta)
#     """
#     # Use the stored file_id to maintain consistency.
#     file_id = stored_file_meta["id"]
#     metadata = extract_basic_metadata(Path(file))

#     extracted_text = extract_text(file, limit = 1000)


#     updated_file_meta = {
#         "id": file_id,
#         "file_name": metadata["file_name"],
#         "original_path": metadata["original_path"],
#         "file_type": metadata["file_type"],
#         "size_kb": metadata["size_kb"],
#         "created_at": metadata["created_at"],
#         "modified_at": metadata["modified_at"],
#         "accessed_at": metadata["accessed_at"],
#         "extracted_text": extracted_text,
#         "upload_date": datetime.now().isoformat(),
#         "hash_md5": metadata["hash_md5"]
#     }


#     return updated_file_meta


# def extract_text_from_pdf(pdf_path, limit=1000) -> str:
#     """
#     Extract up to 'limit' characters of text from a PDF file.

#     This function processes pages one by one and stops as soon as the accumulated
#     text reaches the requested character limit, thereby avoiding processing the
#     entire document unnecessarily.

#     Parameters:
#         pdf_path (str): The path to the PDF file.
#         limit (int): The maximum number of characters to extract.

#     Returns:
#         str: The extracted text (up to the specified limit). Returns an empty string
#              if no text is extracted or an error occurs.
#     """
#     if limit <= 0:
#         return ""

#     try:
#         from PyPDF2 import PdfReader  # Ensure PdfReader is imported here if not already.
#         reader = PdfReader(pdf_path)
#         text_chunks = []
#         remaining = limit

#         for page in reader.pages:
#             if remaining <= 0:
#                 break  # Stop if we've reached the limit.
#             page_text = page.extract_text() or ""
#             if page_text:
#                 # If the current page has more than the remaining characters, take only what is needed.
#                 if len(page_text) > remaining:
#                     text_chunks.append(page_text[:remaining])
#                     remaining = 0
#                 else:
#                     text_chunks.append(page_text)
#                     remaining -= len(page_text)

#         final_text = "".join(text_chunks)
#         if not final_text.strip():
#             logging.warning(f"No text extracted from PDF: {pdf_path}")
#             print(f"WARNING: No text extracted from PDF: {pdf_path}")
#         return final_text
#     except Exception as e:
#         logging.error(f"Error extracting text from PDF {pdf_path}: {e}")
#         print(f"ERROR: Failed to extract text from PDF {pdf_path}: {e}")
#         return ""


# def extract_text(file_path: Path, limit = 1000) -> str:
#     """Extract a small text snippet (first 1000 chars) for categorization."""
#     file_path = str(file_path)  # ✅ Convert Path object to string

#     # # ✅ Ignore unwanted file types
#     # if any(ext in file_path for ext in CHUNK_IGNORED_EXTENSIONS):
#     #     return ""

#     try:
#         if file_path.endswith(".pdf"):
#             return extract_text_from_pdf(file_path, limit = limit)


#         # elif file_path.endswith(".docx"):
#         #     doc = docx.Document(file_path)
#         #     return "\n".join([p.text for p in doc.paragraphs])

#         elif file_path.endswith((".txt", ".log", ".md", ".tex")):
#             with open(file_path, "r", encoding="utf-8") as f:
#                 return f.read(limit)  # ✅ Read first 1000 chars

#         elif file_path.endswith(".py"):
#             with open(file_path, "r", encoding="utf-8") as f:
#                 lines = [line.strip() for line in f.readlines() if not line.strip().startswith("#")]
#                 return "\n".join(lines)[:limit]  # ✅ Skip comments

#         elif file_path.endswith(".ipynb"):
#             with open(file_path, "r", encoding="utf-8") as f:
#                 try:
#                     notebook = json.load(f)
#                 except json.JSONDecodeError:
#                     print(f"⚠️ WARNING: Invalid JSON in {file_path}. Skipping...")
#                     return ""

#                 texts = []
#                 for cell in notebook.get("cells", []):
#                     if isinstance(cell, dict) and cell.get("cell_type") in ("markdown", "code"):
#                         source = cell.get("source", [])
#                         if isinstance(source, list):
#                             texts.append(" ".join(source))
#                         elif isinstance(source, str):
#                             texts.append(source)

#                 return " ".join(texts)[:limit]  # Limit text length

#     except Exception as e:
#         print(f"⚠️ Skipping text extraction for {file_path}: {e}")

#     return ""
