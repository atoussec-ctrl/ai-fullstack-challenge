"""Book use cases."""

from __future__ import annotations

from datetime import date

from app.repositories import BookRepository


def parse_book_payload(payload: dict[str, object]) -> dict[str, object]:
    required = ("title", "author", "summary")
    for field in required:
        if not str(payload.get(field, "")).strip():
            raise ValueError(f"Campo {field} é obrigatório.")

    publication_date = parse_publication_date(payload)

    return {
        "title": str(payload["title"]).strip(),
        "category": str(payload.get("category", "Programação")).strip() or "Programação",
        "author": str(payload["author"]).strip(),
        "publication_date": publication_date,
        "summary": str(payload["summary"]).strip(),
    }


def parse_publication_date(payload: dict[str, object]) -> date:
    raw_date = str(payload.get("publication_date", "")).strip()
    if raw_date:
        try:
            return date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ValueError("Campo publication_date deve usar o formato YYYY-MM-DD.") from exc

    raw_year = str(payload.get("publication_year", payload.get("year", ""))).strip()
    if not raw_year:
        raise ValueError("Campo publication_date ou publication_year é obrigatório.")
    try:
        year = int(raw_year)
    except ValueError as exc:
        raise ValueError("Campo publication_year deve ser um ano numérico.") from exc
    if year < 1000 or year > 9999:
        raise ValueError("Campo publication_year deve conter quatro dígitos.")
    return date(year, 1, 1)


class BookService:
    def __init__(self, repository: BookRepository | None = None) -> None:
        self.repository = repository or BookRepository()

    def create(self, payload: dict[str, object]):
        data = parse_book_payload(payload)
        return self.repository.create(**data)

    def get(self, book_id: str):
        book = self.repository.get(book_id)
        if not book:
            raise ValueError("Livro não encontrado.")
        return book

    def search(
        self,
        title: str | None = None,
        author: str | None = None,
        category: str | None = None,
        query_text: str | None = None,
    ):
        return self.repository.search(
            title=title,
            author=author,
            category=category,
            query_text=query_text,
        )
