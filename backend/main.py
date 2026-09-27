"""
Coding Agent - Main Entry Point
Self-Learning AI Code Generation Engine
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from agent.orchestrator import CodeAgent
from api.routes import router as api_router
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Coding Agent API",
    description="Non-LLM based intelligent code generation engine",
    version="0.1.0"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize configuration
config = Config()

# Initialize the agent
agent: Optional[CodeAgent] = None

@app.on_event("startup")
async def startup_event():
    """Initialize agent on server startup"""
    global agent
    logger.info("🚀 Starting Coding Agent...")
    
    try:
        agent = CodeAgent(config)
        await agent.initialize()
        logger.info("✅ Coding Agent initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    global agent
    if agent:
        logger.info("🛑 Shutting down Coding Agent...")
        await agent.cleanup()
        logger.info("✅ Coding Agent shut down successfully")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_ready": agent is not None
    }

# Include API routes
app.include_router(api_router, prefix="/api")

# Chat endpoint
@app.post("/api/chat")
async def chat(message: str):
    """
    Main chat endpoint for interacting with the agent
    
    Args:
        message: User message/request
        
    Returns:
        Agent response with generated code, analysis, or action results
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        logger.info(f"📨 User message: {message}")
        response = await agent.process_request(message)
        logger.info(f"✅ Agent response: {response}")
        return response
    except Exception as e:
        logger.error(f"❌ Error processing request: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# File upload endpoint for code and images
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """
    Upload files (code, images, configs) for analysis
    
    Args:
        file: File to upload
        description: Optional description of the file
        
    Returns:
        File processing result
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        result = await agent.process_upload(file, description)
        return result
    except Exception as e:
        logger.error(f"❌ Error processing upload: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# Image to code endpoint
@app.post("/api/image-to-code")
async def image_to_code(
    image: UploadFile = File(...),
    framework: str = Form("html"),
    description: Optional[str] = Form(None)
):
    """
    Convert UI mockup/screenshot to code
    
    Args:
        image: Mockup or screenshot image
        framework: Target framework (html, react, flutter, etc.)
        description: Optional description of the design
        
    Returns:
        Generated code for the UI
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        result = await agent.image_to_code(image, framework, description)
        return result
    except Exception as e:
        logger.error(f"❌ Error in image-to-code: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# Code generation endpoint
@app.post("/api/generate-code")
async def generate_code(
    specification: str = Form(...),
    language: str = Form("python"),
    framework: Optional[str] = Form(None)
):
    """
    Generate code from specification
    
    Args:
        specification: Code requirements and description
        language: Target programming language
        framework: Target framework (optional)
        
    Returns:
        Generated code and explanation
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        result = await agent.generate_code(specification, language, framework)
        return result
    except Exception as e:
        logger.error(f"❌ Error generating code: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# Code refactoring endpoint
@app.post("/api/refactor-code")
async def refactor_code(
    code: str = Form(...),
    language: str = Form("python"),
    rules: Optional[str] = Form(None)
):
    """
    Refactor existing code
    
    Args:
        code: Code to refactor
        language: Programming language
        rules: Optional refactoring rules/preferences
        
    Returns:
        Refactored code with explanation
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        result = await agent.refactor_code(code, language, rules)
        return result
    except Exception as e:
        logger.error(f"❌ Error refactoring code: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# Bug fix endpoint
@app.post("/api/fix-bug")
async def fix_bug(
    error_log: str = Form(...),
    code: Optional[str] = Form(None),
    language: Optional[str] = Form("python")
):
    """
    Fix bugs from error logs
    
    Args:
        error_log: Stack trace or error message
        code: Related source code (optional)
        language: Programming language
        
    Returns:
        Fix suggestion and corrected code
    """
    if not agent:
        return JSONResponse(
            {"error": "Agent not initialized"},
            status_code=503
        )
    
    try:
        result = await agent.fix_bug(error_log, code, language)
        return result
    except Exception as e:
        logger.error(f"❌ Error fixing bug: {str(e)}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

# WebSocket for real-time updates
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat and streaming responses
    """
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if not agent:
                await websocket.send_json({"error": "Agent not initialized"})
                continue
            
            # Stream response back
            async for chunk in agent.stream_request(data):
                await websocket.send_json(chunk)
                
    except Exception as e:
        logger.error(f"❌ WebSocket error: {str(e)}")
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🤖 Coding Agent - Non-LLM Code Generation Engine")
    logger.info("=" * 60)
    
    # Load configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "False").lower() == "true"
    
    logger.info(f"🌐 Server will be available at:")
    logger.info(f"   - Local: http://localhost:{port}")
    logger.info(f"   - Network: http://0.0.0.0:{port}")
    logger.info(f"   - Mobile: http://<your-machine-ip>:{port}")
    logger.info("=" * 60)
    
    # Start server
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
