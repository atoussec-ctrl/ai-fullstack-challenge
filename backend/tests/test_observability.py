"""Unit tests closing coverage gaps in app.services.observability.

traceable_if_enabled/current_run_id are also exercised indirectly via
decorators evaluated at module-import time (see the "decorator-time
enablement" note in app/services/observability.py), which makes their
outcome depend on whatever LANGSMITH_TRACING happens to be in the real
environment at import time — not something a test should rely on. These
tests call the functions directly with a controlled env instead.
"""

from __future__ import annotations

import app.services.observability as observability


def test_traceable_if_enabled_returns_identity_wrapper_when_disabled(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    def sample(x: int) -> int:
        return x * 2

    wrapped = observability.traceable_if_enabled("test.op")(sample)

    assert wrapped is sample
    assert wrapped(3) == 6


def test_traceable_if_enabled_wraps_with_langsmith_when_enabled(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    def sample(x: int) -> int:
        return x * 2

    wrapped = observability.traceable_if_enabled("test.op", run_type="tool")(sample)

    assert wrapped(3) == 6


def test_current_run_id_returns_none_when_tracing_disabled(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    assert observability.current_run_id() is None


def test_current_run_id_returns_none_without_an_active_run(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    assert observability.current_run_id() is None


def test_current_run_id_returns_id_when_run_tree_is_active(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    class FakeRunTree:
        id = "run-xyz-789"

    import langsmith.run_helpers as run_helpers

    monkeypatch.setattr(run_helpers, "get_current_run_tree", lambda: FakeRunTree())

    assert observability.current_run_id() == "run-xyz-789"


def test_record_feedback_skips_when_run_id_is_missing(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    result = observability.record_feedback(run_id=None, score=1.0)

    assert result == {"recorded": False, "reason": "Message has no LangSmith trace_id."}


def test_record_feedback_skips_when_tracing_disabled(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    result = observability.record_feedback(run_id="run-123", score=1.0)

    assert result == {"recorded": False, "reason": "LangSmith tracing is disabled."}
