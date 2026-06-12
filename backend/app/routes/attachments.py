"""Attachment routes."""

from pathlib import Path

from flask import Blueprint, Response, request, send_file

from app.models import Attachment
from app.services.uploads import UploadService
from app.utils.http import error_response, validation_error

attachments_bp = Blueprint("attachments", __name__)


@attachments_bp.post("/attachments")
def create_attachment():
    file = request.files.get("file")
    session_id = request.form.get("session_id", "")
    kind = request.form.get("kind") or None
    try:
        attachment = UploadService().save(file=file, session_id=session_id, kind=kind)
    except ValueError as exc:
        return validation_error(str(exc))
    return attachment.to_public_dict(), 201


@attachments_bp.get("/attachments/<attachment_id>")
def get_attachment(attachment_id: str):
    attachment = Attachment.query.get(attachment_id)
    if not attachment:
        return error_response("NOT_FOUND", "Anexo não encontrado.", 404)
    path = Path(attachment.storage_path)
    if not path.exists():
        return error_response("NOT_FOUND", "Arquivo do anexo não encontrado.", 404)
    response: Response = send_file(
        path,
        mimetype=attachment.mime_type,
        as_attachment=True,
        download_name=attachment.filename,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
