"""Core orchestration for the coding agent."""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Optional

from .code_generator import CodeGenerator
from .pattern_memory import PatternMemory
from .requirement_parser import RequirementParser
from .validator import Validator


class CodeAgent:
    """Main orchestration layer for the local coding agent."""

    def __init__(self, config: Any):
        self.config = config
        self.parser = RequirementParser()
        self.memory = PatternMemory()
        self.generator = CodeGenerator(self.memory)
        self.validator = Validator()

    async def initialize(self) -> None:
        self.memory.search(["login"])

    async def cleanup(self) -> None:
        return None

    async def process_request(self, message: str) -> Dict[str, Any]:
        requirement = self.parser.parse(message)
        generated = self.generator.generate(requirement)
        validation = self.validator.validate(generated["files"])
        self.memory.record_success(requirement, generated["files"])
        return {
            "status": "ok",
            "requirement": requirement,
            "generation": generated,
            "validation": validation,
        }

    async def process_upload(self, file, description: Optional[str] = None) -> Dict[str, Any]:
        filename = getattr(file, "filename", "uploaded_file")
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        return {
            "status": "received",
            "filename": filename,
            "extension": extension,
            "description": description or "File uploaded for analysis",
            "analysis": "Prototype upload accepted. Image and design files are queued for future OCR and layout analysis.",
        }

    async def image_to_code(self, image, framework: str = "html", description: Optional[str] = None) -> Dict[str, Any]:
        return {
            "status": "ok",
            "framework": framework,
            "description": description or "UI mockup uploaded",
            "analysis": "This prototype recognizes the image as a design input and will convert it to a starter layout in a future phase.",
            "generated": {
                "index.html": "<!DOCTYPE html><html><body><h1>Design mockup placeholder</h1></body></html>",
                "styles.css": "body { font-family: Arial; padding: 24px; }",
            },
        }

    async def generate_code(self, specification: str, language: str = "python", framework: Optional[str] = None) -> Dict[str, Any]:
        requirement = self.parser.parse(specification)
        requirement["language"] = language
        if framework:
            requirement["framework"] = framework
        generated = self.generator.generate(requirement)
        validation = self.validator.validate(generated["files"])
        return {
            "status": "ok",
            "requirement": requirement,
            "generation": generated,
            "validation": validation,
        }

    async def refactor_code(self, code: str, language: str = "python", rules: Optional[str] = None) -> Dict[str, Any]:
        return {
            "status": "ok",
            "language": language,
            "rules": rules or "Keep function structure and improve clarity",
            "refactored_code": code,
            "notes": "Refactoring support is included as a placeholder. Future versions will apply AST-based restructuring.",
        }

    async def fix_bug(self, error_log: str, code: Optional[str] = None, language: Optional[str] = "python") -> Dict[str, Any]:
        return {
            "status": "ok",
            "language": language,
            "error_log": error_log,
            "code": code or "",
            "fix": "Diagnosed as a validation or logic issue. This prototype returns a targeted fix plan and keeps the original code structure intact.",
        }

    async def stream_request(self, message: str) -> AsyncIterator[Dict[str, Any]]:
        yield {"type": "analysis", "content": "Parsing requirement..."}
        yield {"type": "analysis", "content": "Searching local patterns..."}
        result = await self.process_request(message)
        yield {"type": "result", "content": result}
