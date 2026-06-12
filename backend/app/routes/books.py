"""Book API routes."""

from flask import Blueprint, jsonify, request

from app.services.book_import import BookImportService
from app.services.books import BookService
from app.utils.http import error_response, validation_error

books_bp = Blueprint("books", __name__)


@books_bp.post("/books")
def create_book():
    payload = request.get_json(silent=True) or {}
    try:
        book = BookService().create(payload)
    except ValueError as exc:
        return validation_error(str(exc))
    return jsonify(book.to_dict()), 201


@books_bp.post("/books/import")
def import_book():
    try:
        book, extracted = BookImportService().import_file(request.files.get("file"))
    except ValueError as exc:
        return validation_error(str(exc))
    return jsonify(
        {
            "book": book.to_dict(),
            "extracted": {
                "title": extracted.title,
                "category": extracted.category,
                "author": extracted.author,
                "publication_year": extracted.publication_year,
                "summary": extracted.summary,
            },
        }
    ), 201


@books_bp.get("/books")
def list_books():
    title = request.args.get("title")
    author = request.args.get("author")
    category = request.args.get("category")
    query_text = request.args.get("q")
    books = BookService().search(
        title=title,
        author=author,
        category=category,
        query_text=query_text,
    )
    return jsonify([book.to_dict() for book in books])


@books_bp.get("/books/<book_id>")
def get_book(book_id: str):
    try:
        book = BookService().get(book_id)
    except ValueError:
        return error_response("NOT_FOUND", "Livro não encontrado.", 404)
    return jsonify(book.to_dict())
