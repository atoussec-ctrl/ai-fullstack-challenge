"""Feedback não pode estourar 500 quando o LangSmith recusa a chamada (403 etc.)."""

from __future__ import annotations

import app.services.observability as observability


def test_record_feedback_degrades_gracefully_on_langsmith_error(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    class ExplodingClient:
        def create_feedback(self, **kwargs):
            raise RuntimeError("403 Client Error: Forbidden")

    import langsmith

    monkeypatch.setattr(langsmith, "Client", ExplodingClient)

    result = observability.record_feedback(run_id="run-123", score=1.0)

    assert result["recorded"] is False
    assert "Forbidden" in result["reason"]


def test_feedback_endpoint_returns_202_even_when_langsmith_fails(client, monkeypatch):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]
    payload = client.post(
        "/api/v1/chat/messages",
        json={"session_id": session_id, "content": "oi"},
    ).get_json()
    message_id = payload["assistant_message_id"]

    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    class ExplodingClient:
        def create_feedback(self, **kwargs):
            raise RuntimeError("LangSmith indisponível")

    import langsmith

    monkeypatch.setattr(langsmith, "Client", ExplodingClient)

    response = client.post(
        f"/api/v1/chat/messages/{message_id}/feedback",
        json={"score": 1},
    )

    assert response.status_code == 202
    body = response.get_json()
    assert body["recorded"] is False
