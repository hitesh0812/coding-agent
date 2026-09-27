"""Pattern memory system for the coding agent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class PatternMemory:
    """Stores reusable code patterns and successful implementations."""

    def __init__(self, storage_path: str | None = None):
        self.storage_path = Path(storage_path) if storage_path else Path(__file__).resolve().parents[1] / "data" / "patterns.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.patterns: Dict[str, Any] = self._load_default_patterns()

    def _load_default_patterns(self) -> Dict[str, Any]:
        default_patterns = {
            "login_page": {
                "description": "Simple login page with email and password fields",
                "language": "html",
                "framework": "plain",
                "files": {
                    "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Login</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <main class=\"login-page\">
      <section class=\"login-card\">
        <h1>Welcome back</h1>
        <p>Sign in to continue</p>
        <form>
          <label>
            Email
            <input type=\"email\" placeholder=\"name@example.com\" />
          </label>
          <label>
            Password
            <input type=\"password\" placeholder=\"********\" />
          </label>
          <button type=\"submit\">Sign In</button>
        </form>
      </section>
    </main>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                    "styles.css": """
:root {
  --bg: #0f172a;
  --panel: #111827;
  --primary: #4f46e5;
  --text: #e5e7eb;
  --muted: #9ca3af;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: var(--text);
  font-family: Arial, sans-serif;
}
.login-page {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 24px;
}
.login-card {
  width: min(100%, 420px);
  background: rgba(17, 24, 39, 0.9);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 32px 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.login-card h1 {
  margin: 0 0 8px;
  font-size: 2rem;
}
.login-card p {
  margin: 0 0 24px;
  color: var(--muted);
}
label {
  display: block;
  margin-bottom: 16px;
  font-weight: 600;
}
input {
  width: 100%;
  margin-top: 8px;
  padding: 12px 14px;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  background: rgba(255,255,255,0.04);
  color: var(--text);
}
button {
  width: 100%;
  border: none;
  border-radius: 10px;
  background: var(--primary);
  color: white;
  padding: 14px 16px;
  font-size: 1rem;
  cursor: pointer;
}
""",
                    "script.js": """
document.querySelector('form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  alert('Login submitted');
});
"""
                }
            },
            "todo_app": {
                "description": "Simple to-do list manager",
                "language": "html",
                "framework": "plain",
                "files": {
                    "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>To Do List</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <main class=\"todo-app\">
      <h1>My Tasks</h1>
      <form id=\"task-form\">
        <input id=\"task-input\" type=\"text\" placeholder=\"Add a task\" />
        <button>Add</button>
      </form>
      <ul id=\"task-list\"></ul>
    </main>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                    "styles.css": """
body { font-family: Arial, sans-serif; display: flex; justify-content: center; padding: 40px; }
.todo-app { width: min(100%, 500px); }
#task-form { display: flex; gap: 10px; margin-bottom: 20px; }
#task-input { flex: 1; padding: 10px; }
button { padding: 10px 14px; }
#task-list { list-style: none; padding: 0; }
#task-list li { display: flex; justify-content: space-between; margin-bottom: 12px; }
""",
                    "script.js": """
const form = document.getElementById('task-form');
const input = document.getElementById('task-input');
const list = document.getElementById('task-list');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const value = input.value.trim();
  if (!value) return;
  const item = document.createElement('li');
  item.innerHTML = `<span>${value}</span><button type=\"button\">Done</button>`;
  item.querySelector('button').addEventListener('click', () => item.remove());
  list.appendChild(item);
  input.value = '';
});
"""
                }
            },
            "landing_page": {
                "description": "Product landing page with hero section and call-to-action",
                "language": "html",
                "framework": "plain",
                "files": {
                    "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Product</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <header class=\"hero\">
      <nav>
        <div class=\"brand\">Acme</div>
        <div class=\"nav-links\"><a href=\"#\">Features</a><a href=\"#\">Pricing</a><a href=\"#\">Docs</a></div>
      </nav>
      <div class=\"hero-copy\">
        <h1>Build faster with Acme</h1>
        <p>Ship smarter workflows for your team.</p>
        <button>Get started</button>
      </div>
    </header>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                    "styles.css": """
body { margin: 0; font-family: Arial, sans-serif; }
.hero { background: #101827; color: white; min-height: 80vh; padding: 28px 5%; }
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-links { display: flex; gap: 20px; }
a { color: white; text-decoration: none; }
.hero-copy { margin-top: 80px; max-width: 600px; }
button { background: #4f46e5; color: white; padding: 12px 20px; border: none; border-radius: 8px; }
""",
                    "script.js": """
console.log('Acme landing page loaded');
"""
                }
            }
        }

        if not self.storage_path.exists():
            self.storage_path.write_text(json.dumps(default_patterns, indent=2), encoding="utf-8")
        else:
            try:
                stored = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.patterns = {**default_patterns, **stored}
            except json.JSONDecodeError:
                self.patterns = default_patterns

    def search(self, keywords: List[str]):
        matches = []
        for key, pattern in self.patterns.items():
            haystack = f"{key} {pattern.get('description', '')}".lower()
            score = 0
            for keyword in keywords:
                if keyword.lower() in haystack:
                    score += 1
            if score:
                matches.append({"name": key, "score": score, "pattern": pattern})
        matches.sort(key=lambda item: item["score"], reverse=True)
        return matches[:5]

    def record_success(self, requirement: Dict[str, Any], generated_files: Dict[str, Any]) -> None:
        key = requirement.get("app_type") or "custom_app"
        self.patterns[key] = {
            "description": requirement.get("summary", "custom generated app"),
            "language": requirement.get("language", "html"),
            "framework": requirement.get("framework", "plain"),
            "files": generated_files,
        }
        self.storage_path.write_text(json.dumps(self.patterns, indent=2), encoding="utf-8")


if __name__ == "__main__":
    memory = PatternMemory()
    print(memory.search(["login"]))
