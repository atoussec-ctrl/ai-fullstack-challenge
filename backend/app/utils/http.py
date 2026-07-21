"""HTTP helpers shared by API routes."""

from __future__ import annotations

from flask import jsonify, request

from app.errors import ValidationError

MAX_PAGE_SIZE = 200


def parse_pagination(args) -> tuple[int | None, int | None]:
    """Parse optional `limit`/`offset` query params shared by list endpoints.

    Both are optional and additive — omitting them keeps today's unbounded
    response, so existing clients (and the OpenAPI contract) don't break.
    """
    limit = _parse_non_negative_int(args.get("limit"), "limit", max_value=MAX_PAGE_SIZE)
    offset = _parse_non_negative_int(args.get("offset"), "offset")
    return limit, offset


def _parse_non_negative_int(
    raw: str | None, field: str, *, max_value: int | None = None
) -> int | None:
    if raw is None or raw == "":
        return None
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValidationError(f"Campo {field} deve ser um número inteiro.", field=field) from exc
    if value < 0:
        raise ValidationError(f"Campo {field} não pode ser negativo.", field=field)
    if max_value is not None and value > max_value:
        raise ValidationError(f"Campo {field} não pode exceder {max_value}.", field=field)
    return value


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
