"""Load project-root .env regardless of process working directory."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

_PLACEHOLDER_API_KEYS = frozenset({"", "replace-me", "changeme", "change-me"})


def _normalize_langsmith_env() -> None:
    """Prefer a real API key when legacy or placeholder vars coexist."""
    langsmith_key = os.getenv("LANGSMITH_API_KEY", "").strip()
    langchain_key = os.getenv("LANGCHAIN_API_KEY", "").strip()

    if langsmith_key.lower() in _PLACEHOLDER_API_KEYS and langchain_key:
        os.environ["LANGSMITH_API_KEY"] = langchain_key

    if not os.getenv("LANGSMITH_PROJECT") and os.getenv("LANGCHAIN_PROJECT"):
        os.environ["LANGSMITH_PROJECT"] = os.environ["LANGCHAIN_PROJECT"]

    if os.getenv("LANGSMITH_TRACING", "").lower() == "true":
        os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")


def load_project_env() -> Path | None:
    """Load ``.env`` from the repository root if it exists."""
    if ENV_FILE.is_file():
        load_dotenv(dotenv_path=ENV_FILE)
        _normalize_langsmith_env()
        return ENV_FILE
    return None
