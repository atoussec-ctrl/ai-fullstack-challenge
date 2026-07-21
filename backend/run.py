"""MindSight AI — Application entry-point.

Usage:
    python run.py
"""

from __future__ import annotations

import os

from app.env_loader import load_project_env

load_project_env()

from app import create_app  # noqa: E402

app = create_app()


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=_env_flag("FLASK_DEBUG"))
