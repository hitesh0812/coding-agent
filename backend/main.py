"""Serve the local web UI and generated project workspace."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from agent.orchestrator import CodeAgent
from utils.logger import setup_logger

logger = setup_logger(__name__)
config = Config()
agent: Optional[CodeAgent] = None
app = FastAPI(title="Coding Agent API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup_event():
    global agent
    agent = CodeAgent(config)
    await agent.initialize()
    logger.info("Coding Agent ready; workspace=%s", config.WORKSPACE_DIR)


@app.on_event("shutdown")
async def shutdown_event():
    if agent:
        await agent.cleanup()


@app.get("/")
async def index():
    return FileResponse(config.BASE_DIR / "frontend" / "index.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent_ready": agent is not None, "workspace": str(config.WORKSPACE_DIR)}


def require_agent() -> CodeAgent:
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent


@app.post("/api/chat")
async def chat(payload: dict):
    message = str(payload.get("message", "")).strip()
    if not message:
        raise HTTPException(status_code=400, detail="message is required")
    return await require_agent().process_request(message)


@app.get("/api/projects")
async def list_projects():
    return {"projects": require_agent().workspace.list_projects()}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    try:
        return require_agent().workspace.get_project(project_id)
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_id}/download")
async def download_project(project_id: str):
    try:
        archive = require_agent().workspace.zip_project(project_id)
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return FileResponse(archive, media_type="application/zip", filename=f"{project_id}.zip")


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), description: Optional[str] = Form(None)):
    return await require_agent().process_upload(file, description)


@app.post("/api/image-to-code")
async def image_to_code(image: UploadFile = File(...), framework: str = Form("html"), description: Optional[str] = Form(None)):
    return await require_agent().image_to_code(image, framework, description)


def main():
    uvicorn.run(app, host=config.HOST, port=config.PORT, reload=config.DEBUG, log_level="info")


if __name__ == "__main__":
    main()
