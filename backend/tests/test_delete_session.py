"""TDD: exclusão de sessão de chat (MS-606)."""


def test_delete_session_removes_session_messages_and_attachments(client):
    session_id = client.post("/api/v1/chat/sessions", json={"title": "Apagar"}).get_json()["id"]
    client.post(
        "/api/v1/chat/messages",
        json={"session_id": session_id, "content": "mensagem temporária"},
    )

    response = client.delete(f"/api/v1/chat/sessions/{session_id}")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/api/v1/chat/sessions").get_json() == []
    assert client.get(f"/api/v1/chat/sessions/{session_id}/messages").status_code == 404


def test_delete_session_returns_404_when_missing(client):
    response = client.delete("/api/v1/chat/sessions/session_inexistente")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"
