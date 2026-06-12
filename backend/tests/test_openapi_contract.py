def test_openapi_documents_all_public_routes(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    spec = response.get_json()
    paths = spec["paths"]

    expected = {
        "/api/v1/health",
        "/api/v1/books",
        "/api/v1/books/import",
        "/api/v1/books/{book_id}",
        "/api/v1/chat/sessions",
        "/api/v1/chat/sessions/{session_id}",
        "/api/v1/chat/sessions/{session_id}/messages",
        "/api/v1/chat/messages",
        "/api/v1/chat/messages/{assistant_message_id}/stream",
        "/api/v1/chat/messages/{assistant_message_id}/feedback",
        "/api/v1/attachments",
        "/api/v1/attachments/{attachment_id}",
        "/api/v1/semantic-search",
    }
    assert expected.issubset(paths.keys())
    assert "Book" in spec["components"]["schemas"]
    assert "ErrorResponse" in spec["components"]["schemas"]


def test_swagger_docs_page_points_to_openapi(client):
    response = client.get("/docs")

    assert response.status_code == 200
    assert b"SwaggerUIBundle" in response.data
    assert b"/openapi.json" in response.data
