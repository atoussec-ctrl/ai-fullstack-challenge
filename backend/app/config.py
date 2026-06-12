"""MindSight AI configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def resolve_sqlite_url(value: str) -> str:
    if value.startswith("sqlite:///./"):
        relative_path = value.removeprefix("sqlite:///./")
        return f"sqlite:///{BASE_DIR / relative_path}"
    if value.startswith("sqlite:///") and not value.startswith("sqlite:////"):
        relative_path = value.removeprefix("sqlite:///")
        return f"sqlite:///{BASE_DIR / relative_path}"
    return value


class Config:
    """Base configuration shared by all environments."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JSON_SORT_KEYS: bool = False

    # Database
    SQLALCHEMY_DATABASE_URI: str = resolve_sqlite_url(
        os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'storage' / 'app.db'}")
    )

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    CHAT_GATEWAY: str = os.getenv("CHAT_GATEWAY", "local")

    # LangSmith
    LANGSMITH_TRACING: str = os.getenv("LANGSMITH_TRACING", "false")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT: str = os.getenv("LANGSMITH_PROJECT", "mindsight-ai")

    # Embeddings / Vector Store
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "faiss")
    FAISS_INDEX_PATH: str = os.getenv(
        "FAISS_INDEX_PATH", str(BASE_DIR / "storage" / "faiss.index")
    )

    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "storage" / "uploads"))
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    MAX_CONTENT_LENGTH: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024

    # CORS
    CORS_ALLOWED_ORIGINS: str = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3002,http://127.0.0.1:3002",
    )

    # API
    API_TITLE = "MindSight AI"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"


class DevelopmentConfig(Config):
    """Development-specific settings."""

    DEBUG: bool = True


class TestingConfig(Config):
    """Testing-specific settings — uses in-memory SQLite."""

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    LANGSMITH_TRACING: str = "false"
    OPENAI_API_KEY: str = "test-key"
    CHAT_GATEWAY: str = "local"
    UPLOAD_DIR: str = "/tmp/mindsight-test-uploads"
    FAISS_INDEX_PATH: str = "/tmp/mindsight-test-faiss.index"
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    """Production-specific settings."""

    DEBUG: bool = False


config_by_name: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
