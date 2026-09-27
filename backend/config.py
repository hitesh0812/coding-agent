"""
Configuration Management for Coding Agent
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class"""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    BACKEND_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    TEMPLATES_DIR = BASE_DIR / "templates"
    WORKSPACE_DIR = BASE_DIR / "workspace"
    
    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)
    WORKSPACE_DIR.mkdir(exist_ok=True)
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Agent Configuration
    AGENT_NAME = "CodeAgent"
    AGENT_VERSION = "0.1.0"
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))
    
    # Knowledge Base
    KB_PATTERNS_DB = DATA_DIR / "patterns.db"
    KB_FAISS_INDEX = DATA_DIR / "patterns.faiss"
    KB_BUG_FIXES = DATA_DIR / "bug_fixes.json"
    KB_COMPONENTS = DATA_DIR / "components.json"
    
    # GitHub Configuration (for research)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_API_RATE_LIMIT = 60  # requests per hour for unauthenticated
    MAX_REPOS_TO_CRAWL = int(os.getenv("MAX_REPOS_TO_CRAWL", 100))
    
    # Code Execution
    DOCKER_ENABLED = os.getenv("DOCKER_ENABLED", "True").lower() == "true"
    TIMEOUT_COMPILE = 30  # seconds
    TIMEOUT_TEST = 60     # seconds
    TIMEOUT_EXECUTE = 30  # seconds
    
    # Image Processing
    OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")  # tesseract or easyocr
    IMAGE_MAX_SIZE = 4096  # pixels
    IMAGE_DPI = 150
    
    # Code Generation
    SUPPORTED_LANGUAGES = [
        "python",
        "java",
        "javascript",
        "typescript",
        "html",
        "css",
        "dart",
        "swift",
        "kotlin",
        "csharp"
    ]
    
    SUPPORTED_FRAMEWORKS = {
        "python": ["django", "fastapi", "flask", "bottle"],
        "javascript": ["react", "vue", "angular", "svelte"],
        "typescript": ["nest", "remix", "astro"],
        "html": ["bootstrap", "tailwind", "bulma"],
        "dart": ["flutter"],
        "java": ["spring", "quarkus", "grails"],
        "kotlin": ["ktor"],
        "csharp": ["aspnet", "aspcore"],
    }
    
    # AI Model Configuration (for validation, not generation)
    # We use ML models for classification, not LLM for generation
    USE_ML_MODELS = True
    ML_MODELS = {
        "pattern_classifier": "models/pattern_classifier.pkl",
        "error_detector": "models/error_detector.pkl",
        "code_similarity": "models/code_similarity.pkl",
    }
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = BACKEND_DIR / "logs" / "agent.log"
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    # Performance
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # 1 hour
    BATCH_SIZE = 32
    
    # Features
    FEATURES = {
        "code_generation": True,
        "code_refactoring": True,
        "bug_fixing": True,
        "image_to_code": True,
        "pattern_learning": True,
        "auto_testing": True,
        "auto_validation": True,
    }
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {k: v for k, v in vars(cls).items() if not k.startswith('_')}
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration"""
        # Check if required directories exist
        assert cls.DATA_DIR.exists(), f"Data directory not found: {cls.DATA_DIR}"
        assert cls.TEMPLATES_DIR.exists(), f"Templates directory not found: {cls.TEMPLATES_DIR}"
        
        # Validate language support
        assert len(cls.SUPPORTED_LANGUAGES) > 0, "No supported languages configured"
        
        print("✅ Configuration validated successfully")

if __name__ == "__main__":
    config = Config()
    config.validate()
    print("\n📋 Current Configuration:")
    for key, value in config.to_dict().items():
        if not key.startswith('_'):
            print(f"  {key}: {value}")
