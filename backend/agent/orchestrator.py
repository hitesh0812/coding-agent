"""Core orchestration for the coding agent."""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Optional

from .code_generator import CodeGenerator
from .pattern_memory import PatternMemory
from .requirement_parser import RequirementParser
from .validator import Validator
from .workspace import WorkspaceManager


class CodeAgent:
    """Main orchestration layer for generation, validation, and persistence."""

    def __init__(self, config: Any):
        self.config = config
        self.parser = RequirementParser()
        self.memory = PatternMemory()
        self.generator = CodeGenerator(self.memory)
        self.validator = Validator()
        self.workspace = WorkspaceManager(config.WORKSPACE_DIR)

    async def initialize(self) -> None:
        self.memory.search(["login"])

    async def cleanup(self) -> None:
        return None

    async def process_request(self, message: str) -> Dict[str, Any]:
        requirement = self.parser.parse(message)
        return await self._generate_and_persist(requirement)

    async def _generate_and_persist(self, requirement: Dict[str, object]) -> Dict[str, Any]:
        generated = self.generator.generate(requirement)
        validation = self.validator.validate(generated["files"])
        project = None
        if validation["valid"]:
            project = self.workspace.create_project(
                name=str(requirement.get("app_type", "generated-project")),
                files=generated["files"],
                metadata={
                    "language": generated.get("language"),
                    "framework": generated.get("framework"),
                    "requirement": requirement.get("raw_text"),
                    "validation": validation,
                },
            )
            self.memory.record_success(requirement, generated["files"])
        return {
            "status": "ok" if validation["valid"] else "validation_failed",
            "requirement": requirement,
            "generation": generated,
            "validation": validation,
            "project": project,
        }

    async def process_upload(self, file, description: Optional[str] = None) -> Dict[str, Any]:
        filename = getattr(file, "filename", "uploaded_file")
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        return {"status": "received", "filename": filename, "extension": extension,
                "description": description or "File uploaded for analysis",
                "analysis": "Upload accepted. Image and design analysis can be added to this workspace pipeline."}

    async def image_to_code(self, image, framework: str = "html", description: Optional[str] = None) -> Dict[str, Any]:
        requirement = self.parser.parse(description or "Create a landing page from this design")
        requirement["framework"] = framework
        result = await self._generate_and_persist(requirement)
        result["image"] = {"filename": getattr(image, "filename", "design")}
        return result

    async def generate_code(self, specification: str, language: str = "python", framework: Optional[str] = None) -> Dict[str, Any]:
        requirement = self.parser.parse(specification)
        requirement["language"] = language
        if framework:
            requirement["framework"] = framework
        return await self._generate_and_persist(requirement)

    async def refactor_code(self, code: str, language: str = "python", rules: Optional[str] = None) -> Dict[str, Any]:
        return {"status": "ok", "language": language, "rules": rules or "Improve clarity", "refactored_code": code,
                "notes": "AST-based refactoring is the next extension point."}

    async def fix_bug(self, error_log: str, code: Optional[str] = None, language: Optional[str] = "python") -> Dict[str, Any]:
        return {"status": "ok", "language": language, "error_log": error_log, "code": code or "",
                "fix": "Bug-fix planning is available; automatic patches will be added with language validators."}

    async def stream_request(self, message: str) -> AsyncIterator[Dict[str, Any]]:
        yield {"type": "analysis", "content": "Parsing requirement..."}
        yield {"type": "analysis", "content": "Searching local patterns..."}
        yield {"type": "result", "content": await self.process_request(message)}
