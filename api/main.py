# api/main.py

import os

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.router import router as api_router

headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
res = requests.get("https://api.openai.com/v1/models", headers=headers)
# print("🔍 Can list models:", res.status_code, res.text)


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

# 🌍 Enable CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Include your core API
app.include_router(api_router)


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


@app.get("/_test/prompty")
def test_prompty_simple():
    from promptflow.core import Prompty

    prompty = Prompty.load("pipeline_core/prompts/translate_to_spanish.prompty")
    try:
        result = prompty(text_input="Hello!")
        return {"success": True, "result": result}
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
