"""LangSmith observability helpers with safe no-op fallbacks."""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def langsmith_enabled() -> bool:
    return os.getenv("LANGSMITH_TRACING", "false").lower() == "true"


def traceable_if_enabled(
    name: str,
    run_type: str = "chain",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    if not langsmith_enabled():
        return lambda function: function

    try:
        from langsmith import traceable
    except ImportError:
        return lambda function: function

    return traceable(name=name, run_type=run_type)


def current_run_id() -> str | None:
    if not langsmith_enabled():
        return None
    try:
        from langsmith.run_helpers import get_current_run_tree
    except ImportError:
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
    except ImportError:
        return {"recorded": False, "reason": "LangSmith package is not installed."}

    try:
        client = Client()
        feedback = client.create_feedback(
            run_id=run_id,
            key=key,
            score=score,
            comment=comment,
        )
    except Exception as exc:
        # Chave inválida/403, rede fora etc. não podem derrubar o endpoint.
        return {"recorded": False, "reason": f"Falha ao enviar ao LangSmith: {exc}"}
    return {"recorded": True, "feedback_id": str(feedback.id)}
