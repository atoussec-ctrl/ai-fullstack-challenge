def test_create_and_search_books(client):
    response = client.post(
        "/api/v1/books",
        json={
            "title": "Python Fluente",
            "category": "Programação",
            "author": "Luciano Ramalho",
            "publication_date": "2015-08-20",
            "summary": "Livro avançado sobre Python.",
        },
    )

    assert response.status_code == 201
    created = response.get_json()
    assert created["id"]
    assert created["title"] == "Python Fluente"
    assert created["category"] == "Programação"
    assert created["publication_year"] == 2015

    by_title = client.get("/api/v1/books?title=python").get_json()
    by_author = client.get("/api/v1/books?author=luciano").get_json()
    by_query = client.get("/api/v1/books?q=avançado").get_json()

    assert len(by_title) == 1
    assert len(by_author) == 1
    assert len(by_query) == 1
    assert by_title[0]["publication_date"] == "2015-08-20"

    detail = client.get(f"/api/v1/books/{created['id']}")
    assert detail.status_code == 200
    assert detail.get_json()["author"] == "Luciano Ramalho"


def test_import_book_from_uploaded_metadata_file(client):
    from io import BytesIO

    content = b"""Titulo: Arquitetura Limpa em Python
Autor: Ana Silva
Categoria: Arquitetura
Ano: 2021
Resumo: Guia pratico para organizar projetos Python com casos de uso, testes e camadas.
"""

    response = client.post(
        "/api/v1/books/import",
        data={"file": (BytesIO(content), "arquitetura.md")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["book"]["title"] == "Arquitetura Limpa em Python"
    assert payload["book"]["category"] == "Arquitetura"
    assert payload["book"]["publication_year"] == 2021


def test_create_book_validates_required_fields(client):
    response = client.post("/api/v1/books", json={"title": "Sem autor"})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
