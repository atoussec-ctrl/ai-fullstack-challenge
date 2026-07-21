"""Health route under the versioned API prefix."""

from flask import Blueprint, jsonify

from app.request_id import current_request_id

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "python-ai-assistant",
            "request_id": current_request_id(),
        }
    )
