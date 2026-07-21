"""Upload validation and storage."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.errors import NotFoundError, ValidationError
from app.extensions import db
from app.models import Attachment
from app.repositories import ChatRepository

ALLOWED_EXTENSIONS: dict[str, set[str]] = {
    "document": {"txt", "md", "py", "json", "pdf"},
    "image": {"png", "jpg", "jpeg", "webp"},
    "audio": {"webm", "wav", "mp3"},
}

ALLOWED_MIME_PREFIXES = {
    "document": ("text/", "application/json", "application/pdf"),
    "image": ("image/png", "image/jpeg", "image/webp"),
    "audio": ("audio/", "video/webm"),
}

# Extensões de documento legíveis como texto puro.
TEXT_EXTRACTABLE_EXTENSIONS = {"txt", "md", "py", "json"}
MAX_ATTACHMENT_TEXT_CHARS = 4000


def read_attachment_text(attachment: Attachment) -> str | None:
    """Return the attachment's text content for AI context, when extractable."""
    if attachment.kind != "document":
        return None
    extension = extension_for(attachment.filename)
    try:
        if extension == "pdf":
            from app.services.book_import import extract_pdf_text

            raw = Path(attachment.storage_path).read_bytes()
            text = extract_pdf_text(raw)
        elif extension in TEXT_EXTRACTABLE_EXTENSIONS:
            text = Path(attachment.storage_path).read_text(encoding="utf-8", errors="ignore")
        else:
            return None
    except OSError:
        return None
    text = text.strip()
    if not text:
        return None
    return text[:MAX_ATTACHMENT_TEXT_CHARS]


def extension_for(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def infer_kind(filename: str, mime_type: str) -> str | None:
    ext = extension_for(filename)
    for kind, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return kind
    for kind, prefixes in ALLOWED_MIME_PREFIXES.items():
        if mime_type and any(mime_type.startswith(prefix) for prefix in prefixes):
            return kind
    return None


class UploadService:
    def __init__(self, chat_repository: ChatRepository | None = None) -> None:
        self.chat_repository = chat_repository or ChatRepository()

    def save(self, *, file: FileStorage, session_id: str, kind: str | None = None) -> Attachment:
        session = self.chat_repository.get_session(session_id)
        if not session:
            raise NotFoundError("Sessão de chat não encontrada.")
        if not file or not file.filename:
            raise ValidationError("Campo file é obrigatório.", field="file")

        original_name = secure_filename(file.filename) or "attachment"
        mime_type = file.mimetype or "application/octet-stream"
        detected_kind = kind or infer_kind(original_name, mime_type)
        if detected_kind not in ALLOWED_EXTENSIONS:
            raise ValidationError("Tipo de anexo inválido.", field="kind")

        ext = extension_for(original_name)
        if ext not in ALLOWED_EXTENSIONS[detected_kind]:
            raise ValidationError("Extensão de arquivo não permitida.", field="file")

        max_bytes = int(current_app.config["MAX_UPLOAD_SIZE_MB"]) * 1024 * 1024
        upload_dir = Path(current_app.config["UPLOAD_DIR"])
        upload_dir.mkdir(parents=True, exist_ok=True)

        storage_name = f"{uuid4().hex}.{ext}"
        storage_path = upload_dir / storage_name
        file.save(storage_path)
        size = storage_path.stat().st_size
        if size > max_bytes:
            storage_path.unlink(missing_ok=True)
            raise ValidationError("Arquivo excede o tamanho máximo permitido.", field="file")

        attachment = Attachment(
            session_id=session_id,
            filename=original_name,
            mime_type=mime_type,
            size=size,
            kind=detected_kind,
            storage_path=str(storage_path),
        )
        db.session.add(attachment)
        db.session.commit()  # this is the whole use case — commits its own unit of work
        return attachment

    def delete_unlinked(self, attachment_id: str) -> None:
        """Remove an attachment that was uploaded but never linked to a message.

        Backstop for the two-request upload-then-send flow: if sending the
        message fails (network, validation, or a partial multi-file upload
        batch), the client calls this to clean up what it just uploaded
        instead of leaving orphaned rows and files behind. Refuses to touch
        an attachment that's already part of a real conversation.
        """
        attachment = self.chat_repository.get_attachment(attachment_id)
        if not attachment:
            raise NotFoundError("Anexo não encontrado.")
        if attachment.message_id is not None:
            raise ValidationError("Anexo já vinculado a uma mensagem.", field="attachment_id")

        storage_path = Path(attachment.storage_path)
        db.session.delete(attachment)
        db.session.commit()
        storage_path.unlink(missing_ok=True)
