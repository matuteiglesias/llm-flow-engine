# api/main.py

import os
import socket
import requests
from fastapi import FastAPI, Request, HTTPException# api/main.py

import os
import socket
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ✅ Core API router
from api.router import router as api_router


# ✅ External check: OpenAI
headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}"}
try:
    res = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=3)
    print("🔍 OpenAI model list accessible:", res.status_code)
except Exception as e:
    print("⚠️  Failed to reach OpenAI:", e)

# ✅ App metadata
app = FastAPI(
    title="AI Workflow MVP",
    description="A modular system to run AI prompt flows using Prompty blocks.",
    version="0.2.0",
    contact={
        "name": "Matías Iglesias",
        "url": "http://matuteiglesias.link",
        "email": "contact@yourdomain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ✅ CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Only your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount routers
app.include_router(api_router)
# if flow_backend:
#     app.include_router(flow_backend.router, prefix="/api")



# ✅ Optionally load routes from modules if they exist
try:
    from api.routes import flow_backend
    app.include_router(flow_backend.router, prefix="/api")
except ImportError:
    flow_backend = None
    print("⚠️  flow_backend could not be imported. Skipping...")

    
@app.get("/")
def read_root():
    return {"message": "Hello from AI Workflow MVP 👋"}


# 🧪 Debug route to see available endpoints
@app.get("/_debug/routes")
def list_routes():
    return [
        {"path": r.path, "name": r.name, "methods": list(r.methods)} for r in app.routes
    ]


from api.router import router as api_router


# ✅ External check: OpenAI
headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}"}
try:
    res = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=3)
    print("🔍 OpenAI model list accessible:", res.status_code)
except Exception as e:
    print("⚠️  Failed to reach OpenAI:", e)

# ✅ App metadata
app = FastAPI(
    title="AI Workflow MVP",
    description="A modular system to run AI prompt flows using Prompty blocks.",
    version="0.2.0",
    contact={
        "name": "Matías Iglesias",
        "url": "http://matuteiglesias.link",
        "email": "contact@yourdomain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ✅ CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Only your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount routers
app.include_router(api_router)
# if flow_backend:
#     app.include_router(flow_backend.router, prefix="/api")



# ✅ Optionally load routes from modules if they exist
try:
    from api.routes import flow_backend
    app.include_router(flow_backend.router, prefix="/api")
except ImportError:
    flow_backend = None
    print("⚠️  flow_backend could not be imported. Skipping...")


@app.get("/")
def read_root():
    return {"message": "Hello from AI Workflow MVP 👋"}


# 🧪 Debug route to see available endpoints
@app.get("/_debug/routes")
def list_routes():
    return [
        {"path": r.path, "name": r.name, "methods": list(r.methods)} for r in app.routes
    ]


# 🔍 Log incoming requests (useful during dev)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    print(f"🚀 {request.method} {request.url.path} - {body.decode()}")
    response = await call_next(request)
    return response


@app.get("/healthz")
def health_check():
    import socket

    try:
        ip = socket.gethostbyname("api.openai.com")
        return {"status": "ok", "openai_ip": ip}
    except Exception as e:
        return {"status": "fail", "error": str(e)}

from fastapi import Request, Query
from typing import Optional
from promptflow.core import Prompty

@app.get("/_test/prompty")
def test_prompty_simple(
    text_input: str = Query(..., description="Text to translate"),
    model_name: Optional[str] = Query("gpt-3.5-turbo", description="Model name"),   ###
    temperature: Optional[float] = Query(0.3, description="Model temperature"),
    max_tokens: Optional[int] = Query(512, description="Max token limit")
):
    try:
        prompty = Prompty.load(
            "pipeline_core/prompts/translate_to_spanish.prompty",
            model={
                "api": "chat",
                "configuration": {
                    "type": "openai",
                    "model": model_name,
                },
                "parameters": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            },
        )

        result = prompty(text_input=text_input)
        rendered = prompty.render(text_input=text_input)

        return {
            "success": True,
            "input": text_input,
            "rendered_prompt": rendered,
            "model_used": model_name,
            "result": result,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


import openai


@app.get("/api/status")
def status():
    import os

    return {
        "status": "ok",
        "env": dict(os.environ),
        "models_loaded": [m.id for m in openai.Model.list().data],
    }


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"🔍 {request.method} {request.url}")
    return await call_next(request)
