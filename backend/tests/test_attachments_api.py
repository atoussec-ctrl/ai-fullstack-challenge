from io import BytesIO


def test_upload_attachment_validates_and_hides_storage_path(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]

    response = client.post(
        "/api/v1/attachments",
        data={
            "session_id": session_id,
            "kind": "document",
            "file": (BytesIO(b"print('hello')"), "example.py"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["kind"] == "document"
    assert payload["filename"] == "example.py"
    assert "storage_path" not in payload
    assert payload["url"].startswith("/api/v1/attachments/")


def test_upload_rejects_dangerous_extension(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]

    response = client.post(
        "/api/v1/attachments",
        data={
            "session_id": session_id,
            "kind": "document",
            "file": (BytesIO(b"bad"), "payload.exe"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
