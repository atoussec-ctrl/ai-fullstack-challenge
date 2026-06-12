"""Persistence repositories."""

from __future__ import annotations

import re
from datetime import date

from app.extensions import db
from app.models import Attachment, Book, ChatMessage, ChatSession, utc_now


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
        db.session.commit()
        return book

    def get(self, book_id: str) -> Book | None:
        return db.session.get(Book, book_id)

    def search(
        self,
        title: str | None = None,
        author: str | None = None,
        category: str | None = None,
        query_text: str | None = None,
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
                return books
            return sorted(
                [book for book in books if score_book(book, terms) > 0],
                key=lambda book: score_book(book, terms),
                reverse=True,
            )
        return query.order_by(Book.created_at.desc()).all()

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
    def list_sessions(self) -> list[ChatSession]:
        return ChatSession.query.order_by(ChatSession.updated_at.desc()).all()

    def get_session(self, session_id: str) -> ChatSession | None:
        return db.session.get(ChatSession, session_id)

    def create_session(self, title: str = "Nova conversa") -> ChatSession:
        session = ChatSession(title=title.strip() or "Nova conversa")
        db.session.add(session)
        db.session.commit()
        return session

    def list_messages(self, session_id: str) -> list[ChatMessage]:
        return (
            ChatMessage.query.filter_by(session_id=session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

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
        db.session.commit()
        return message

    def find_attachments(self, attachment_ids: list[str]) -> list[Attachment]:
        return Attachment.query.filter(Attachment.id.in_(attachment_ids)).all()

    def attach_to_message(self, attachment_ids: list[str], message_id: str) -> list[Attachment]:
        attachments = self.find_attachments(attachment_ids)
        for attachment in attachments:
            attachment.message_id = message_id
        db.session.commit()
        return attachments
