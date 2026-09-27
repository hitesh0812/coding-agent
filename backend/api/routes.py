"""API routes for the coding agent."""

from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.get("/status")
async def status():
    return {
        "status": "ok",
        "service": "coding-agent",
        "features": [
            "requirement_parsing",
            "pattern_memory",
            "code_generation",
            "validation",
            "image_upload_support",
        ],
    }


@router.post("/chat")
async def chat(payload: ChatRequest):
    return {
        "status": "ok",
        "message": payload.message,
        "response": "This prototype is ready to generate starter code from the requirement using local pattern and validation logic.",
    }


@router.post("/upload")
async def upload(file: UploadFile = File(...), description: str | None = Form(None)):
    return {
        "status": "received",
        "filename": file.filename,
        "description": description,
        "message": "Upload accepted for analysis in the prototype pipeline.",
    }
