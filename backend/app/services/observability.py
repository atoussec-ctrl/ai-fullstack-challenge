"""LangSmith observability helpers with safe no-op fallbacks."""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from flask import current_app, has_app_context

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def langsmith_enabled() -> bool:
    # Decorators (traceable_if_enabled) call this at module-import time, with
    # no request/app context yet, so os.getenv is the only option there.
    # At request time, prefer Flask config so per-environment overrides
    # (e.g. TestingConfig forcing tracing off) are respected even though
    # app/config.py now eagerly loads the real .env into os.environ.
    if has_app_context():
        return str(current_app.config.get("LANGSMITH_TRACING", "false")).lower() == "true"
    return os.getenv("LANGSMITH_TRACING", "false").lower() == "true"


def traceable_if_enabled(
    name: str,
    run_type: str = "chain",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if not langsmith_enabled():
        return lambda function: function

    try:
        from langsmith import traceable
    except ImportError:  # pragma: no cover - langsmith is a required dependency
        return lambda function: function

    return traceable(name=name, run_type=run_type)


def current_run_id() -> str | None:
    if not langsmith_enabled():
        return None
    try:
        from langsmith.run_helpers import get_current_run_tree
    except ImportError:  # pragma: no cover - langsmith is a required dependency
        return None

    run_tree = get_current_run_tree()
    if not run_tree:
        return None
    return str(run_tree.id)


def record_feedback(
    *,
    run_id: str | None,
    score: float,
    key: str = "user_score",
    comment: str | None = None,
) -> dict[str, object]:
    if not langsmith_enabled():
        return {"recorded": False, "reason": "LangSmith tracing is disabled."}
    if not run_id:
        return {"recorded": False, "reason": "Message has no LangSmith trace_id."}

    try:
        from langsmith import Client
    except ImportError:  # pragma: no cover - langsmith is a required dependency
        return {"recorded": False, "reason": "LangSmith package is not installed."}

    try:
        client = Client()
        feedback = client.create_feedback(
            run_id=run_id,
            key=key,
            score=score,
            comment=comment,
        )
    except Exception:
        # Chave inválida/403, rede fora etc. não podem derrubar o endpoint, e o
        # detalhe da exceção não deve vazar para o cliente — só para o log.
        logger.exception("Falha ao enviar feedback ao LangSmith (run_id=%s)", run_id)
        return {
            "recorded": False,
            "reason": "Não foi possível registrar o feedback no momento.",
        }
    return {"recorded": True, "feedback_id": str(feedback.id)}
