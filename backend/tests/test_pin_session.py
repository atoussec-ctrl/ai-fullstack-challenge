"""TDD: pin/unpin de sessão de chat."""


def test_patch_session_pins_and_unpins(client):
    session_id = client.post("/api/v1/chat/sessions", json={"title": "Fixar"}).get_json()["id"]

    pin_response = client.patch(
        f"/api/v1/chat/sessions/{session_id}",
        json={"pinned": True},
    )
    assert pin_response.status_code == 200
    pinned = pin_response.get_json()
    assert pinned["pinned"] is True
    assert pinned["pinned_at"] is not None

    unpin_response = client.patch(
        f"/api/v1/chat/sessions/{session_id}",
        json={"pinned": False},
    )
    assert unpin_response.status_code == 200
    unpinned = unpin_response.get_json()
    assert unpinned["pinned"] is False
    assert unpinned["pinned_at"] is None


def test_patch_session_returns_404_when_missing(client):
    response = client.patch(
        "/api/v1/chat/sessions/session_inexistente",
        json={"pinned": True},
    )

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"


def test_patch_session_requires_pinned_field(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]

    response = client.patch(f"/api/v1/chat/sessions/{session_id}", json={})

    assert response.status_code == 400
    assert response.get_json()["error"]["details"]["field"] == "pinned"


def test_patch_session_rejects_non_boolean_pinned(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]

    response = client.patch(f"/api/v1/chat/sessions/{session_id}", json={"pinned": "sim"})

    assert response.status_code == 400
    assert response.get_json()["error"]["details"]["field"] == "pinned"
