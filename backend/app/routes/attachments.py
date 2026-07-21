"""Attachment routes."""

from pathlib import Path

from flask import Blueprint, Response, request, send_file

from app.errors import NotFoundError
from app.repositories import ChatRepository
from app.services.uploads import UploadService

attachments_bp = Blueprint("attachments", __name__)


@attachments_bp.post("/attachments")
def create_attachment():
    file = request.files.get("file")
    session_id = request.form.get("session_id", "")
    kind = request.form.get("kind") or None
    attachment = UploadService().save(file=file, session_id=session_id, kind=kind)
    return attachment.to_public_dict(), 201


@attachments_bp.get("/attachments/<attachment_id>")
def get_attachment(attachment_id: str):
    attachment = ChatRepository().get_attachment(attachment_id)
    if not attachment:
        raise NotFoundError("Anexo não encontrado.")
    path = Path(attachment.storage_path)
    if not path.exists():
        raise NotFoundError("Arquivo do anexo não encontrado.")
    response: Response = send_file(
        path,
        mimetype=attachment.mime_type,
        as_attachment=True,
        download_name=attachment.filename,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
