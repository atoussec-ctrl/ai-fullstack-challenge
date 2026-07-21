"""Chat session and message routes."""

from __future__ import annotations

import json
import time

from flask import Blueprint, Response, jsonify, request

from app.repositories import ChatRepository
from app.services.chat import ChatService
from app.services.observability import record_feedback
from app.utils.http import error_response, parse_pagination, validation_error

chat_bp = Blueprint("chat", __name__)


@chat_bp.get("/chat/sessions")
def list_sessions():
    limit, offset = parse_pagination(request.args)
    sessions = ChatRepository().list_sessions(limit=limit, offset=offset)
    return jsonify([session.to_dict() for session in sessions])


@chat_bp.post("/chat/sessions")
def create_session():
    payload = request.get_json(silent=True) or {}
    session = ChatService().create_session(str(payload.get("title", "Nova conversa")))
    return jsonify(session.to_dict()), 201


@chat_bp.delete("/chat/sessions/<session_id>")
def delete_session(session_id: str):
    ChatService().delete_session(session_id)
    return "", 204


@chat_bp.patch("/chat/sessions/<session_id>")
def update_session(session_id: str):
    payload = request.get_json(silent=True) or {}
    if "pinned" not in payload:
        return validation_error("Campo pinned é obrigatório.", "pinned")
    if not isinstance(payload["pinned"], bool):
        return validation_error("Campo pinned deve ser booleano.", "pinned")

    session = ChatService().update_session(session_id, pinned=payload["pinned"])
    return jsonify(session.to_dict())


@chat_bp.get("/chat/sessions/<session_id>/messages")
def list_messages(session_id: str):
    repository = ChatRepository()
    if not repository.get_session(session_id):
        return error_response("NOT_FOUND", "Sessão de chat não encontrada.", 404)
    limit, offset = parse_pagination(request.args)
    messages = repository.list_messages(session_id, limit=limit, offset=offset)
    return jsonify([message.to_dict() for message in messages])


@chat_bp.post("/chat/messages")
def create_message():
    if request.content_type and request.content_type.startswith("multipart/form-data"):
        payload = request.form
        attachment_ids = request.form.getlist("attachment_ids")
    else:
        payload = request.get_json(silent=True) or {}
        attachment_ids = list(payload.get("attachment_ids", []) or [])

    session_id = str(payload.get("session_id", "")).strip()
    if not session_id:
        return validation_error("Campo session_id é obrigatório.", "session_id")

    user_message, assistant_message = ChatService(
        model=str(payload.get("model", "")).strip() or None
    ).ask(
        session_id=session_id,
        content=str(payload.get("content", "")),
        thinking_mode=str(payload.get("thinking_mode", "balanced")),
        attachment_ids=attachment_ids,
    )

    return jsonify(
        {
            "user_message_id": user_message.id,
            "assistant_message_id": assistant_message.id,
            "status": assistant_message.status,
            "assistant_message": assistant_message.to_dict(),
        }
    ), 201


@chat_bp.get("/chat/messages/<assistant_message_id>/stream")
def stream_message(assistant_message_id: str):
    message = ChatRepository().get_message(assistant_message_id)
    if not message:
        return error_response("NOT_FOUND", "Mensagem não encontrada.", 404)

    def generate():
        if message.status == "failed":
            yield (
                "event: error\n"
                f"data: {json.dumps({'message_id': message.id, 'content': message.content})}\n\n"
            )
            return
        for token in message.content.split(" "):
            yield f"event: token\ndata: {json.dumps({'content': token + ' '})}\n\n"
            time.sleep(0.001)
        yield f"event: done\ndata: {json.dumps({'message_id': message.id})}\n\n"

    response = Response(generate(), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@chat_bp.post("/chat/messages/<assistant_message_id>/feedback")
def create_feedback(assistant_message_id: str):
    message = ChatRepository().get_message(assistant_message_id)
    if not message:
        return error_response("NOT_FOUND", "Mensagem não encontrada.", 404)

    payload = request.get_json(silent=True) or {}
    try:
        score = float(payload.get("score"))
    except (TypeError, ValueError):
        return validation_error("Campo score deve ser numérico.", "score")
    if score < -1 or score > 1:
        return validation_error("Campo score deve estar entre -1 e 1.", "score")

    result = record_feedback(
        run_id=message.trace_id,
        score=score,
        key=str(payload.get("key", "user_score")),
        comment=str(payload.get("comment", "")).strip() or None,
    )
    return result, 202
