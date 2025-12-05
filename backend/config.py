"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"


def get_openrouter_api_key() -> str:
    """Get OpenRouter API key from settings or environment."""
    from .settings import get_settings
    settings = get_settings()
    if settings.openrouter_api_key:
        return settings.openrouter_api_key
    return os.getenv("OPENROUTER_API_KEY", "")


def get_ollama_base_url() -> str:
    """Get Ollama base URL from settings."""
    from .settings import get_settings
    return get_settings().ollama_base_url


def get_council_models() -> list:
    """Get council models from settings."""
    from .settings import get_settings, DEFAULT_COUNCIL_MODELS
    settings = get_settings()
    return settings.council_models or DEFAULT_COUNCIL_MODELS


def get_chairman_model() -> str:
    """Get chairman model from settings."""
    from .settings import get_settings, DEFAULT_CHAIRMAN_MODEL
    settings = get_settings()
    return settings.chairman_model or DEFAULT_CHAIRMAN_MODEL


# Database settings
def get_database_config() -> dict:
    """Get database configuration from environment."""
    db_type = os.getenv("DB_TYPE", "json").lower()
    return {
        "type": db_type,
        "url": os.getenv("DATABASE_URL")
    }

# Tool settings
def get_tool_config() -> dict:
    """Get tool configuration from environment."""
    return {
        "enable_tools": os.getenv("ENABLE_TOOLS", "true").lower() == "true",  # Default ON
        "available_tools": os.getenv("AVAILABLE_TOOLS", "calculator,wikipedia,arxiv,finance").split(","),
        "tavily_api_key": os.getenv("TAVILY_API_KEY")
    }

# Document settings
def get_document_config() -> dict:
    """Get document configuration."""
    return {
        "max_upload_size": int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024)),  # 10MB default
        "upload_dir": os.path.join(os.getcwd(), "data", "documents")
    }

# Classification settings
def get_classification_config() -> dict:
    """Get Stage 0 classification configuration."""
    return {
        "enabled": os.getenv("ENABLE_CLASSIFICATION", "true").lower() == "true",
        "confidence_threshold": float(os.getenv("CLASSIFICATION_CONFIDENCE", "0.7"))
    }

# Strategy settings
def get_strategy_config() -> dict:
    """Get deliberation strategy configuration."""
    return {
        "default_strategy": os.getenv("DEFAULT_STRATEGY", "simple"),  # simple, multi_round
        "multi_round_rounds": int(os.getenv("MULTI_ROUND_ROUNDS", "2"))
    }

COUNCIL_MODELS = [
    "openai/gpt-4.1",
    "google/gemini-2.5-pro",
    "anthropic/claude-sonnet-4",
    "x-ai/grok-3",
]
CHAIRMAN_MODEL = "google/gemini-2.5-pro"
