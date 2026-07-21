"""Persistence repositories."""

from __future__ import annotations

import re
from datetime import date

from app.extensions import db
from app.models import Attachment, Book, ChatMessage, ChatSession, utc_now


def _paginate(items: list, limit: int | None, offset: int | None) -> list:
    """Slice an in-memory list for the branches that can't paginate in SQL
    (free-text search ranks in Python after loading candidate rows)."""
    start = offset or 0
    end = start + limit if limit is not None else None
    return items[start:end]


class BookRepository:
    def create(
        self,
        *,
        title: str,
        category: str,
        author: str,
        publication_date: date,
        summary: str,
    ) -> Book:
        book = Book(
            title=title,
            category=category,
            author=author,
            publication_date=publication_date,
            summary=summary,
        )
        db.session.add(book)
        db.session.flush()
        return book

    def get(self, book_id: str) -> Book | None:
        return db.session.get(Book, book_id)

    def search(
        self,
        title: str | None = None,
        author: str | None = None,
        category: str | None = None,
        query_text: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Book]:
        query = Book.query
        if title:
            query = query.filter(Book.title.ilike(f"%{title.strip()}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author.strip()}%"))
        if category:
            query = query.filter(Book.category.ilike(f"%{category.strip()}%"))
        if query_text:
            terms = search_terms(query_text)
            books = query.order_by(Book.created_at.desc()).all()
            if not terms:
                return _paginate(books, limit, offset)
            ranked = sorted(
                [book for book in books if score_book(book, terms) > 0],
                key=lambda book: score_book(book, terms),
                reverse=True,
            )
            return _paginate(ranked, limit, offset)
        query = query.order_by(Book.created_at.desc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def relevant_for_question(self, question: str, limit: int = 3) -> list[Book]:
        terms = search_terms(question)
        if not terms:
            return []
        books = Book.query.order_by(Book.created_at.desc()).all()
        ranked = sorted(
            ((score_book(book, terms), book) for book in books),
            key=lambda item: item[0],
            reverse=True,
        )
        return [book for score, book in ranked[:limit] if score > 0]


STOPWORDS = {
    "como",
    "qual",
    "quais",
    "sobre",
    "livro",
    "livros",
    "resumo",
    "resuma",
    "explique",
    "autor",
    "autora",
    "data",
    "publicacao",
    "publicação",
    "python",
    "para",
    "com",
    "dos",
    "das",
    "uma",
    "uns",
    "que",
    "tem",
}


def search_terms(text: str) -> list[str]:
    tokens = re.findall(r"[\wÀ-ÿ]+", text.lower())
    return [token for token in tokens if len(token) >= 3 and token not in STOPWORDS]


def score_book(book: Book, terms: list[str]) -> int:
    haystack = f"{book.title} {book.category} {book.author} {book.summary}".lower()
    score = 0
    for term in terms:
        if term in book.title.lower():
            score += 4
        if term in book.category.lower():
            score += 3
        if term in book.author.lower():
            score += 3
        score += haystack.count(term)
    return score


class ChatRepository:
    def list_sessions(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[ChatSession]:
        query = ChatSession.query.order_by(
            ChatSession.pinned.desc(),
            ChatSession.pinned_at.desc(),
            ChatSession.updated_at.desc(),
        )
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_session(self, session_id: str) -> ChatSession | None:
        return db.session.get(ChatSession, session_id)

    def create_session(self, title: str = "Nova conversa") -> ChatSession:
        session = ChatSession(title=title.strip() or "Nova conversa")
        db.session.add(session)
        db.session.flush()
        return session

    def delete_session(self, session_id: str) -> bool:
        session = self.get_session(session_id)
        if not session:
            return False
        db.session.delete(session)
        db.session.flush()
        return True

    def update_session(
        self,
        session_id: str,
        *,
        pinned: bool | None = None,
    ) -> ChatSession | None:
        session = self.get_session(session_id)
        if not session:
            return None
        if pinned is not None:
            session.pinned = pinned
            session.pinned_at = utc_now() if pinned else None
        db.session.flush()
        return session

    def list_messages(
        self, session_id: str, limit: int | None = None, offset: int | None = None
    ) -> list[ChatMessage]:
        query = ChatMessage.query.filter_by(session_id=session_id).order_by(
            ChatMessage.created_at.asc()
        )
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def get_message(self, message_id: str) -> ChatMessage | None:
        return db.session.get(ChatMessage, message_id)

    def create_message(
        self,
        *,
        session_id: str,
        role: str,
        content: str,
        thinking_mode: str | None = None,
        status: str = "completed",
        trace_id: str | None = None,
    ) -> ChatMessage:
        created_at = utc_now()
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            thinking_mode=thinking_mode,
            status=status,
            trace_id=trace_id,
            created_at=created_at,
        )
        session = self.get_session(session_id)
        if session:
            session.updated_at = created_at
        db.session.add(message)
        db.session.flush()
        return message

    def get_attachment(self, attachment_id: str) -> Attachment | None:
        return db.session.get(Attachment, attachment_id)

    def find_attachments(self, attachment_ids: list[str]) -> list[Attachment]:
        return Attachment.query.filter(Attachment.id.in_(attachment_ids)).all()

    def attach_to_message(self, attachment_ids: list[str], message_id: str) -> list[Attachment]:
        attachments = self.find_attachments(attachment_ids)
        for attachment in attachments:
            attachment.message_id = message_id
        db.session.flush()
        return attachments
