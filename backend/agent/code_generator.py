"""Code generation utilities for the coding agent."""

from __future__ import annotations

from typing import Dict, List

from .pattern_memory import PatternMemory


class CodeGenerator:
    """Creates starter code files from parsed requirements."""

    def __init__(self, memory: PatternMemory | None = None):
        self.memory = memory or PatternMemory()

    def generate(self, requirement: Dict[str, object]) -> Dict[str, object]:
        app_type = str(requirement.get("app_type", "custom_app"))
        language = str(requirement.get("language", "html"))

        matched = self.memory.search([app_type.replace("_", " ")])
        if matched and matched[0]["pattern"]["files"]:
            pattern_files = matched[0]["pattern"]["files"]
            files = {k: v for k, v in pattern_files.items()}
            return {
                "language": language,
                "framework": requirement.get("framework", "plain"),
                "app_type": app_type,
                "files": files,
                "source": "pattern_memory",
                "strategy": "matched_pattern",
            }

        files = self._generate_default_files(app_type, language)
        return {
            "language": language,
            "framework": requirement.get("framework", "plain"),
            "app_type": app_type,
            "files": files,
            "source": "template",
            "strategy": "default_generation",
        }

    def _generate_default_files(self, app_type: str, language: str) -> Dict[str, str]:
        if app_type == "login_page":
            return {
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
    <main class=\"login-layout\">
      <div class=\"login-box\">
        <h1>Login</h1>
        <form>
          <input type=\"email\" placeholder=\"Email\" />
          <input type=\"password\" placeholder=\"Password\" />
          <button type=\"submit\">Sign In</button>
        </form>
      </div>
    </main>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                "styles.css": """
body { margin: 0; font-family: Arial; background: linear-gradient(120deg, #111827, #1f2937); color: white; }
.login-layout { min-height: 100vh; display: grid; place-items: center; }
.login-box { width: min(100%, 420px); background: rgba(255,255,255,0.06); padding: 32px; border-radius: 14px; }
input, button { width: 100%; box-sizing: border-box; padding: 12px; margin-top: 14px; border-radius: 8px; }
input { border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.04); color: white; }
button { background: #4f46e5; color: white; border: none; }
""",
                "script.js": """
document.querySelector('form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  alert('Login form submitted');
});
""",
            }

        if app_type == "todo_app":
            return {
                "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Tasks</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <main class=\"todo-container\">
      <h1>Task Board</h1>
      <form id=\"task-form\">
        <input type=\"text\" id=\"task-input\" placeholder=\"Add a task\" />
        <button type=\"submit\">Add</button>
      </form>
      <ul id=\"task-list\"></ul>
    </main>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                "styles.css": """
body { margin: 0; font-family: Arial; background: #f8fafc; padding: 30px; }
.todo-container { max-width: 640px; margin: 0 auto; }
#task-form { display: flex; gap: 10px; margin-top: 20px; }
#task-input { flex: 1; padding: 10px; }
button { padding: 10px 14px; }
#task-list { list-style: none; padding: 0; margin-top: 20px; }
#task-list li { display: flex; justify-content: space-between; background: white; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
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
""",
            }

        if app_type == "landing_page":
            return {
                "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Acme</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <header class=\"hero\">
      <nav>
        <div class=\"brand\">Acme</div>
        <div class=\"nav-links\"><a href=\"#\">Product</a><a href=\"#\">Pricing</a><a href=\"#\">Support</a></div>
      </nav>
      <div class=\"hero-content\">
        <h1>Build your next idea faster</h1>
        <p>Ship product features without friction.</p>
        <button>Get Started</button>
      </div>
    </header>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
                "styles.css": """
body { margin: 0; font-family: Arial, sans-serif; }
.hero { padding: 24px 5%; min-height: 75vh; background: #0f172a; color: white; }
nav { display: flex; justify-content: space-between; align-items: center; }
.nav-links { display: flex; gap: 24px; }
a { color: white; text-decoration: none; }
.hero-content { margin-top: 80px; max-width: 640px; }
button { margin-top: 16px; background: #4f46e5; color: white; padding: 12px 24px; border: none; border-radius: 8px; }
""",
                "script.js": """
console.log('Landing page ready');
""",
            }

        return {
            "index.html": """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>Generated App</title>
    <link rel=\"stylesheet\" href=\"styles.css\" />
  </head>
  <body>
    <main>
      <h1>Generated App</h1>
      <p>Your custom app shell is ready.</p>
    </main>
    <script src=\"script.js\"></script>
  </body>
</html>
""",
            "styles.css": """
body { font-family: Arial, sans-serif; padding: 25px; }
main { max-width: 700px; margin: 0 auto; }
""",
            "script.js": """
console.log('Generated app initialized');
""",
        }
