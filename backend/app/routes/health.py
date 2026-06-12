"""Health route under the versioned API prefix."""

from flask import Blueprint, jsonify, request

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "python-ai-assistant",
            "request_id": request.headers.get("X-Request-ID"),
        }
    )
