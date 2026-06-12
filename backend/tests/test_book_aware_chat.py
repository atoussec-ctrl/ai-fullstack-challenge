def test_chat_uses_books_as_local_context(client):
    book_response = client.post(
        "/api/v1/books",
        json={
            "title": "Python Fluente",
            "category": "Programação",
            "author": "Luciano Ramalho",
            "publication_date": "2015-08-20",
            "summary": "Livro avançado sobre data model, iteradores e Python idiomático.",
        },
    )
    assert book_response.status_code == 201

    session_id = client.post("/api/v1/chat/sessions", json={"title": "Livros"}).get_json()["id"]
    response = client.post(
        "/api/v1/chat/messages",
        json={
            "session_id": session_id,
            "content": "Resuma o livro Python Fluente e cite autor e publicação.",
            "thinking_mode": "deep",
        },
    )

    assert response.status_code == 201
    content = response.get_json()["assistant_message"]["content"]
    assert "Python Fluente" in content
    assert "Programação" in content
    assert "Luciano Ramalho" in content
    assert "2015-08-20" in content
    assert "biblioteca local" in content
