"""HTTP helpers shared by API routes."""

from __future__ import annotations

from flask import jsonify, request


def error_response(
    code: str,
    message: str,
    status_code: int = 400,
    details: dict[str, object] | None = None,
):
    payload = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
        "request_id": request.headers.get("X-Request-ID"),
    }
    return jsonify(payload), status_code


def validation_error(message: str, field: str | None = None):
    details: dict[str, object] = {}
    if field:
        details["field"] = field
    return error_response("VALIDATION_ERROR", message, 400, details)
