def test_create_session_send_message_and_stream(client):
    session_response = client.post("/api/v1/chat/sessions", json={"title": "Listas"})
    assert session_response.status_code == 201
    session_id = session_response.get_json()["id"]

    message_response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": session_id,
            "content": "Como criar uma lista em Python?",
            "thinking_mode": "balanced",
        },
    )

    assert message_response.status_code == 201
    payload = message_response.get_json()
    assert payload["status"] == "completed"
    assert "lista" in payload["assistant_message"]["content"].lower()
    assert "trace_id" in payload["assistant_message"]

    messages = client.get(f"/api/v1/chat/sessions/{session_id}/messages").get_json()
    assert [message["role"] for message in messages] == ["user", "assistant"]

    stream = client.get(f"/api/v1/chat/messages/{payload['assistant_message_id']}/stream")
    assert stream.status_code == 200
    assert b"event: token" in stream.data
    assert b"event: done" in stream.data

    feedback = client.post(
        f"/api/v1/chat/messages/{payload['assistant_message_id']}/feedback",
        json={"score": 1, "comment": "boa resposta"},
    )
    assert feedback.status_code == 202
    assert feedback.get_json()["recorded"] is False


def test_chat_rejects_invalid_thinking_mode(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]

    response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": session_id,
            "content": "Oi",
            "thinking_mode": "slow",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
