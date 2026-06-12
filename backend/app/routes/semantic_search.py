"""Semantic search routes."""

from flask import Blueprint, jsonify, request

from app.services.semantic_search import SemanticSearchService
from app.utils.http import validation_error

semantic_search_bp = Blueprint("semantic_search", __name__)


@semantic_search_bp.post("/semantic-search")
def semantic_search():
    payload = request.get_json(silent=True) or {}
    try:
        results = SemanticSearchService().search(
            query=str(payload.get("query", "")),
            k=int(payload.get("k", 3)),
        )
    except (TypeError, ValueError) as exc:
        return validation_error(str(exc))
    return jsonify({"results": results})
