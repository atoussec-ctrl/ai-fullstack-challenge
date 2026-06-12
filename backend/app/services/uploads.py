"""Upload validation and storage."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

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

# Extensões de documento legíveis como texto puro (PDF é binário e fica de fora).
TEXT_EXTRACTABLE_EXTENSIONS = {"txt", "md", "py", "json"}
MAX_ATTACHMENT_TEXT_CHARS = 4000


def read_attachment_text(attachment: Attachment) -> str | None:
    """Return the attachment's text content for AI context, when extractable."""
    if attachment.kind != "document":
        return None
    if extension_for(attachment.filename) not in TEXT_EXTRACTABLE_EXTENSIONS:
        return None
    try:
        text = Path(attachment.storage_path).read_text(encoding="utf-8", errors="ignore")
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
            raise ValueError("Sessão de chat não encontrada.")
        if not file or not file.filename:
            raise ValueError("Campo file é obrigatório.")

        original_name = secure_filename(file.filename) or "attachment"
        mime_type = file.mimetype or "application/octet-stream"
        detected_kind = kind or infer_kind(original_name, mime_type)
        if detected_kind not in ALLOWED_EXTENSIONS:
            raise ValueError("Tipo de anexo inválido.")

        ext = extension_for(original_name)
        if ext not in ALLOWED_EXTENSIONS[detected_kind]:
            raise ValueError("Extensão de arquivo não permitida.")

        max_bytes = int(current_app.config["MAX_UPLOAD_SIZE_MB"]) * 1024 * 1024
        upload_dir = Path(current_app.config["UPLOAD_DIR"])
        upload_dir.mkdir(parents=True, exist_ok=True)

        storage_name = f"{uuid4().hex}.{ext}"
        storage_path = upload_dir / storage_name
        file.save(storage_path)
        size = storage_path.stat().st_size
        if size > max_bytes:
            storage_path.unlink(missing_ok=True)
            raise ValueError("Arquivo excede o tamanho máximo permitido.")

        attachment = Attachment(
            session_id=session_id,
            filename=original_name,
            mime_type=mime_type,
            size=size,
            kind=detected_kind,
            storage_path=str(storage_path),
        )
        db.session.add(attachment)
        db.session.commit()
        return attachment
