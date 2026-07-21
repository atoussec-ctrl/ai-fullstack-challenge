"""TDD: exclusão de sessão de chat (MS-606)."""

from io import BytesIO
from pathlib import Path

from app.extensions import db
from app.models import Attachment


def test_delete_session_removes_session_messages_and_attachments(client, app):
    session_id = client.post("/api/v1/chat/sessions", json={"title": "Apagar"}).get_json()["id"]
    upload = client.post(
        "/api/v1/attachments",
        data={"session_id": session_id, "file": (BytesIO(b"temporario"), "temp.txt")},
        content_type="multipart/form-data",
    )
    assert upload.status_code == 201
    attachment_id = upload.get_json()["id"]
    client.post(
        "/api/v1/chat/messages",
        json={"session_id": session_id, "content": "mensagem temporária"},
    )

    with app.app_context():
        attachment = db.session.get(Attachment, attachment_id)
        storage_path = Path(attachment.storage_path)
        assert storage_path.exists()

    response = client.delete(f"/api/v1/chat/sessions/{session_id}")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/api/v1/chat/sessions").get_json() == []
    assert client.get(f"/api/v1/chat/sessions/{session_id}/messages").status_code == 404
    assert not storage_path.exists()


def test_chat_repository_delete_session_returns_false_when_missing(app):
    from app.repositories import ChatRepository

    with app.app_context():
        assert ChatRepository().delete_session("sessao-que-nao-existe") is False


def test_delete_session_returns_404_when_missing(client):
    response = client.delete("/api/v1/chat/sessions/session_inexistente")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"
