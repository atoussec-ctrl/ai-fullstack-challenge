def test_semantic_search_returns_relevant_python_documents(client):
    response = client.post(
        "/api/v1/semantic-search",
        json={"query": "Como guardar vários itens em Python?", "k": 3},
    )

    assert response.status_code == 200
    results = response.get_json()["results"]
    assert len(results) == 3
    assert any(result["document_id"] == "doc_lists" for result in results)


def test_semantic_search_validates_empty_query(client):
    response = client.post("/api/v1/semantic-search", json={"query": "", "k": 3})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
