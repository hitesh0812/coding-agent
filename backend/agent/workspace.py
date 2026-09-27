"""Safe filesystem workspace management for generated projects."""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable


class WorkspaceManager:
    """Persists generated projects below one controlled workspace directory."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def create_project(self, name: str, files: Dict[str, str], metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        project_id = f"{self._slug(name)}-{uuid.uuid4().hex[:8]}"
        project_dir = self.root / project_id
        project_dir.mkdir(parents=True)

        written = []
        for relative_path, content in files.items():
            destination = self._safe_path(project_dir, relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(str(content), encoding="utf-8")
            written.append(str(destination.relative_to(project_dir)))

        project_metadata = {
            "id": project_id,
            "name": name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "files": sorted(written),
            **(metadata or {}),
        }
        (project_dir / ".coding-agent.json").write_text(
            json.dumps(project_metadata, indent=2), encoding="utf-8"
        )
        return project_metadata

    def list_projects(self) -> list[Dict[str, Any]]:
        projects = []
        for directory in sorted(self.root.iterdir(), reverse=True):
            metadata_file = directory / ".coding-agent.json"
            if directory.is_dir() and metadata_file.exists():
                try:
                    projects.append(json.loads(metadata_file.read_text(encoding="utf-8")))
                except json.JSONDecodeError:
                    continue
        return projects

    def get_project(self, project_id: str) -> Dict[str, Any]:
        project_dir = self._project_dir(project_id)
        metadata_file = project_dir / ".coding-agent.json"
        if not metadata_file.exists():
            raise FileNotFoundError("Project metadata not found")
        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        metadata["files"] = {
            path: (project_dir / path).read_text(encoding="utf-8")
            for path in metadata.get("files", [])
            if (project_dir / path).is_file()
        }
        return metadata

    def zip_project(self, project_id: str) -> Path:
        project_dir = self._project_dir(project_id)
        archive_path = Path(tempfile.gettempdir()) / f"{project_id}.zip"
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in project_dir.rglob("*"):
                if file_path.is_file() and file_path.name != ".coding-agent.json":
                    archive.write(file_path, file_path.relative_to(project_dir))
        return archive_path

    def _project_dir(self, project_id: str) -> Path:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,80}", project_id):
            raise ValueError("Invalid project id")
        directory = self._safe_path(self.root, project_id)
        if not directory.is_dir():
            raise FileNotFoundError("Project not found")
        return directory

    @staticmethod
    def _slug(value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
        return (slug or "generated-project")[:45]

    @staticmethod
    def _safe_path(root: Path, relative_path: str) -> Path:
        candidate = (root / relative_path).resolve()
        if candidate != root and root not in candidate.parents:
            raise ValueError(f"Unsafe path: {relative_path}")
        if Path(relative_path).is_absolute():
            raise ValueError("Absolute paths are not allowed")
        return candidate
