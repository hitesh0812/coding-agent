# Coding Agent - Self-Learning AI Code Generation

A non-LLM based intelligent coding agent that generates, refactors, and fixes code by learning from repositories, code examples, and images. The project is designed to run locally on macOS, iPhone, Android, or any device through a local-host web interface with internet access for research.

## What this prototype does

This initial version is a working MVP focused on a practical architecture:

- Accepts a requirement in plain language
- Parses it into features, app type, language, and framework
- Searches a local pattern library for similar implementations
- Generates a working starter app for HTML/CSS/JavaScript
- Validates the generated output
- Provides a local API and chat interface
- Supports uploads for image references and design sketches
- Can be extended with extra languages and repo research later

## Project layout

```text
coding-agent/
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── code_generator.py
│   │   ├── orchestrator.py
│   │   ├── pattern_memory.py
│   │   ├── requirement_parser.py
│   │   └── validator.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── data/
│   └── patterns.json
├── README.md
└── .gitignore
```

## Run locally

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Then open:

- http://localhost:8000/health
- http://localhost:8000/api/status
- http://localhost:8000/static/index.html (after static hosting is enabled)

## Example request

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "message=Create a login page with email and password fields and a sign-in button"
```

## Notes

This is intentionally a non-LLM design. The agent learns through:

- static code pattern matching
- structured requirement parsing
- repository-like pattern libraries
- validation feedback
- stored successful implementations

It is not a general-purpose LLM replacement yet, but it is a real code-generation engine foundation for the architecture you requested.

## Roadmap

- Add repo crawling and GitHub pattern research
- Expand language support to Python, Java, Dart, and Flutter templates
- Add image-to-code conversion from upload
- Add bug-fix and refactoring engine
- Add stronger validation and code repair loops
- Add a React or mobile client for richer interaction
