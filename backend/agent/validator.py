"""Validation logic for generated code."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Dict


class Validator:
    """Quick validation of code quality and structure."""

    def validate(self, files: Dict[str, str]) -> Dict[str, Any]:
        errors = []
        warnings = []

        for filename, content in files.items():
            if filename.endswith(".py"):
                try:
                    ast.parse(content)
                except SyntaxError as exc:
                    errors.append(f"{filename}: {exc.msg} at line {exc.lineno}")
            elif filename.endswith(".html"):
                if "<html" not in content.lower():
                    warnings.append(f"{filename}: HTML document structure may be incomplete")
                if "<title" not in content.lower():
                    warnings.append(f"{filename}: Missing title tag")
            elif filename.endswith(".css"):
                if "{" not in content or "}" not in content:
                    warnings.append(f"{filename}: CSS block structure looks incomplete")

        valid = len(errors) == 0
        return {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
            "message": "Validation passed" if valid else "Validation failed",
        }
