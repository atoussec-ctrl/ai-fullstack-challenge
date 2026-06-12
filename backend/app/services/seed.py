"""Idempotent database seeding.

Safe to run multiple times: a book is only created when no existing book has
the same (title, author) pair, so re-seeding never duplicates or overwrites
existing data.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.services.books import BookService

DEFAULT_BOOKS: list[dict[str, object]] = [
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Engenharia de Software",
        "publication_year": 2008,
        "summary": (
            "Princípios, padrões e práticas para escrever código limpo, legível "
            "e de fácil manutenção."
        ),
    },
    {
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "category": "Arquitetura de Software",
        "publication_year": 2017,
        "summary": (
            "Regras de dependência, fronteiras e camadas para sistemas sustentáveis e testáveis."
        ),
    },
    {
        "title": "Python Fluente",
        "author": "Luciano Ramalho",
        "category": "Programação",
        "publication_year": 2015,
        "summary": ("Uso idiomático de Python: data model, iteradores, decorators e concorrência."),
    },
    {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "category": "Engenharia de Software",
        "publication_year": 2018,
        "summary": (
            "Catálogo de refatorações para melhorar o design de código existente com segurança."
        ),
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt e David Thomas",
        "category": "Engenharia de Software",
        "publication_year": 1999,
        "summary": (
            "Boas práticas pragmáticas de desenvolvimento, automação e "
            "responsabilidade profissional."
        ),
    },
]


@dataclass(frozen=True)
class SeedResult:
    created: int
    skipped: int

    @property
    def total(self) -> int:
        return self.created + self.skipped


def seed_books(
    books: list[dict[str, object]] | None = None,
    book_service: BookService | None = None,
) -> SeedResult:
    """Insert sample books idempotently. Returns counts of created/skipped."""
    service = book_service or BookService()
    catalog = DEFAULT_BOOKS if books is None else books

    existing = {
        (book.title.strip().lower(), book.author.strip().lower()) for book in service.search()
    }

    created = 0
    skipped = 0
    for payload in catalog:
        key = (
            str(payload["title"]).strip().lower(),
            str(payload["author"]).strip().lower(),
        )
        if key in existing:
            skipped += 1
            continue
        service.create(payload)
        existing.add(key)
        created += 1

    return SeedResult(created=created, skipped=skipped)
