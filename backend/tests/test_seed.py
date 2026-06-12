"""Seed deve popular o catálogo sem duplicar dados existentes."""

from __future__ import annotations

from app.services.books import BookService
from app.services.seed import DEFAULT_BOOKS, seed_books


def test_seed_is_idempotent(app):
    with app.app_context():
        first = seed_books()
        assert first.created == len(DEFAULT_BOOKS)
        assert first.skipped == 0

        # Segunda execução não cria nada novo.
        second = seed_books()
        assert second.created == 0
        assert second.skipped == len(DEFAULT_BOOKS)

        books = BookService().search()
        assert len(books) == len(DEFAULT_BOOKS)


def test_seed_preserves_existing_books(app):
    with app.app_context():
        service = BookService()
        service.create(
            {
                "title": "Meu Livro Manual",
                "author": "Autor Local",
                "category": "Romance",
                "publication_year": 2020,
                "summary": "Conteúdo que não pode ser perdido no seed.",
            }
        )

        result = seed_books()

        assert result.created == len(DEFAULT_BOOKS)
        titles = {book.title for book in service.search()}
        assert "Meu Livro Manual" in titles
        assert len(titles) == len(DEFAULT_BOOKS) + 1
