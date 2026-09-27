"""Requirement parser for the coding agent."""

from __future__ import annotations

import re
from typing import Dict, List


class RequirementParser:
    """Converts a user request into a structured task description."""

    def parse(self, text: str) -> Dict[str, object]:
        clean_text = (text or "").strip()
        if not clean_text:
            raise ValueError("Request cannot be empty")

        lower_text = clean_text.lower()

        features: List[str] = []
        keyword_map = {
            "login": "login",
            "signup": "signup",
            "register": "signup",
            "dashboard": "dashboard",
            "todo": "todo",
            "task": "todo",
            "landing": "landing_page",
            "homepage": "landing_page",
            "portfolio": "portfolio",
            "shop": "shop",
            "store": "shop",
            "chat": "chat",
            "search": "search",
            "crud": "crud",
            "api": "api",
            "admin": "admin",
            "profile": "profile",
            "contact": "contact",
            "form": "form",
            "button": "button",
            "mobile": "mobile",
            "flutter": "flutter",
            "python": "python",
            "java": "java",
            "javascript": "javascript",
            "typescript": "typescript",
            "html": "html",
            "css": "css",
            "dart": "dart",
        }

        for keyword, value in keyword_map.items():
            if keyword in lower_text:
                features.append(value)

        language = "html"
        if "python" in lower_text:
            language = "python"
        elif "java" in lower_text:
            language = "java"
        elif "flutter" in lower_text or "dart" in lower_text:
            language = "dart"
        elif "typescript" in lower_text:
            language = "typescript"
        elif "javascript" in lower_text:
            language = "javascript"

        framework = "plain"
        if "react" in lower_text:
            framework = "react"
        elif "flutter" in lower_text:
            framework = "flutter"
        elif "fastapi" in lower_text:
            framework = "fastapi"
        elif "django" in lower_text:
            framework = "django"

        app_type = "custom_app"
        if "login" in lower_text:
            app_type = "login_page"
        elif "todo" in lower_text or "task" in lower_text:
            app_type = "todo_app"
        elif "landing" in lower_text or "homepage" in lower_text or "hero" in lower_text:
            app_type = "landing_page"
        elif "dashboard" in lower_text:
            app_type = "dashboard"

        if not features:
            features = ["custom_ui"]

        return {
            "raw_text": clean_text,
            "summary": clean_text,
            "language": language,
            "framework": framework,
            "app_type": app_type,
            "features": _normalize_features(features),
            "word_count": len(re.findall(r"\b\w+\b", clean_text)),
        }


def _normalize_features(items: List[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


if __name__ == "__main__":
    parser = RequirementParser()
    print(parser.parse("Create a login page with email and password fields and a sign in button"))
