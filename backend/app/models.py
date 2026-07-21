"""Database models for the MindSight AI backend."""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import uuid4

from app.extensions import db


def generate_id(prefix: str | None = None) -> str:
    value = uuid4().hex
    return f"{prefix}_{value}" if prefix else value


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def isoformat(value: datetime | date | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=UTC).isoformat().replace("+00:00", "Z")
    return value.isoformat()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.String(64), primary_key=True, default=lambda: generate_id())
    title = db.Column(db.String(255), nullable=False, index=True)
    category = db.Column(db.String(120), nullable=False, default="Programação", index=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    publication_date = db.Column(db.Date, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    def to_dict(self) -> dict[str, str | None]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "author": self.author,
            "publication_date": isoformat(self.publication_date),
            "publication_year": self.publication_date.year if self.publication_date else None,
            "summary": self.summary,
            "created_at": isoformat(self.created_at),
        }


class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.String(96), primary_key=True, default=lambda: generate_id("session"))
    title = db.Column(db.String(255), nullable=False, default="Nova conversa")
    pinned = db.Column(db.Boolean, nullable=False, default=False)
    pinned_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    messages = db.relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )
    attachments = db.relationship(
        "Attachment",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict[str, str | bool | None]:
        return {
            "id": self.id,
            "title": self.title,
            "pinned": self.pinned,
            "pinned_at": isoformat(self.pinned_at) if self.pinned_at else None,
            "created_at": isoformat(self.created_at),
            "updated_at": isoformat(self.updated_at),
        }


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.String(96), primary_key=True, default=lambda: generate_id("msg"))
    session_id = db.Column(
        db.String(96),
        db.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    thinking_mode = db.Column(db.String(32), nullable=True)
    status = db.Column(db.String(32), nullable=False, default="completed")
    trace_id = db.Column(db.String(128), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    session = db.relationship("ChatSession", back_populates="messages")
    attachments = db.relationship(
        "Attachment",
        back_populates="message",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "thinking_mode": self.thinking_mode,
            "status": self.status,
            "trace_id": self.trace_id,
            "attachments": [attachment.to_public_dict() for attachment in self.attachments],
            "created_at": isoformat(self.created_at),
        }


class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.String(96), primary_key=True, default=lambda: generate_id("att"))
    session_id = db.Column(
        db.String(96),
        db.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    message_id = db.Column(
        db.String(96),
        # CASCADE matches the ORM-level cascade="all, delete-orphan" already
        # declared on ChatMessage.attachments below — an attachment without
        # its message has no reason to exist. Previously this said SET NULL,
        # contradicting the ORM cascade (only the ORM path was ever actually
        # exercised, since SQLite FK enforcement isn't enabled here, but the
        # declared DDL should still say what actually happens).
        db.ForeignKey("chat_messages.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(32), nullable=False)
    storage_path = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    session = db.relationship("ChatSession", back_populates="attachments")
    message = db.relationship("ChatMessage", back_populates="attachments")

    def to_public_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "filename": self.filename,
            "mime_type": self.mime_type,
            "size": self.size,
            "kind": self.kind,
            "url": f"/api/v1/attachments/{self.id}",
            "created_at": isoformat(self.created_at),
        }
