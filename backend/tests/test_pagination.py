"""TDD: additive limit/offset pagination on list endpoints.

Backward compatible on purpose — omitting limit/offset keeps today's
unbounded response, so existing clients and the OpenAPI contract don't break.
"""

from __future__ import annotations


def _create_book(client, title, year):
    return client.post(
        "/api/v1/books",
        json={
            "title": title,
            "author": "Autor",
            "summary": "Resumo.",
            "publication_year": year,
        },
    )


# ── /api/v1/books ──


def test_books_list_without_pagination_returns_everything(client):
    for i in range(5):
        _create_book(client, f"Livro {i}", 2000 + i)

    response = client.get("/api/v1/books")

    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_books_list_respects_limit_and_offset(client):
    for i in range(5):
        _create_book(client, f"Livro {i}", 2000 + i)

    page = client.get("/api/v1/books?limit=2&offset=1")

    assert page.status_code == 200
    assert len(page.get_json()) == 2


def test_books_search_by_query_text_also_respects_pagination(client):
    for i in range(5):
        _create_book(client, "Python Avançado", 2000 + i)

    page = client.get("/api/v1/books?q=python&limit=2")

    assert page.status_code == 200
    assert len(page.get_json()) == 2


def test_books_list_rejects_negative_limit(client):
    response = client.get("/api/v1/books?limit=-1")

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["details"]["field"] == "limit"


def test_books_list_rejects_non_numeric_offset(client):
    response = client.get("/api/v1/books?offset=abc")

    assert response.status_code == 400
    assert response.get_json()["error"]["details"]["field"] == "offset"


def test_books_list_rejects_limit_above_max_page_size(client):
    response = client.get("/api/v1/books?limit=99999")

    assert response.status_code == 400
    assert response.get_json()["error"]["details"]["field"] == "limit"


# ── /api/v1/chat/sessions ──


def test_chat_sessions_list_respects_limit_and_offset(client):
    for i in range(4):
        client.post("/api/v1/chat/sessions", json={"title": f"Sessão {i}"})

    page = client.get("/api/v1/chat/sessions?limit=2")

    assert page.status_code == 200
    assert len(page.get_json()) == 2


def test_chat_sessions_list_offset_without_limit_skips_items(client):
    for i in range(4):
        client.post("/api/v1/chat/sessions", json={"title": f"Sessão {i}"})

    all_sessions = client.get("/api/v1/chat/sessions").get_json()
    page = client.get("/api/v1/chat/sessions?offset=1")

    assert len(page.get_json()) == len(all_sessions) - 1


# ── /api/v1/chat/sessions/{id}/messages ──


def test_chat_messages_list_respects_limit_and_offset(client):
    session_id = client.post("/api/v1/chat/sessions", json={}).get_json()["id"]
    for i in range(3):
        client.post("/api/v1/chat/messages", json={"session_id": session_id, "content": f"msg {i}"})

    all_messages = client.get(f"/api/v1/chat/sessions/{session_id}/messages").get_json()
    page = client.get(f"/api/v1/chat/sessions/{session_id}/messages?limit=2&offset=1")

    assert len(all_messages) == 6  # 3 user + 3 assistant messages
    assert page.status_code == 200
    assert len(page.get_json()) == 2
    assert [m["id"] for m in page.get_json()] == [m["id"] for m in all_messages[1:3]]
