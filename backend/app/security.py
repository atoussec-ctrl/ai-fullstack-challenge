"""Minimal shared-secret authentication for the HTTP API.

A single operator-configured API_KEY gates every route except health checks
and CORS preflight. Leaving API_KEY unset (the default) keeps local
development and CI fully open, matching this project's "no external key
required" DX goal — the gate only activates once an operator opts in by
setting it, which production startup then requires (see
app.config.assert_production_config_is_safe).
"""

from __future__ import annotations

from flask import Flask, current_app, request

from app.errors import AuthenticationError

EXEMPT_PATHS = frozenset({"/health", "/api/v1/health"})
_BEARER_PREFIX = "Bearer "


def register_api_key_guard(app: Flask) -> None:
    app.before_request(_enforce_api_key)


def _enforce_api_key() -> None:
    configured_key = current_app.config.get("API_KEY", "")
    if not configured_key:
        return
    if request.method == "OPTIONS" or request.path in EXEMPT_PATHS:
        return
    if _extract_bearer_token(request.headers.get("Authorization", "")) != configured_key:
        raise AuthenticationError("Credencial de API ausente ou inválida.")


def _extract_bearer_token(header_value: str) -> str:
    if not header_value.startswith(_BEARER_PREFIX):
        return ""
    return header_value.removeprefix(_BEARER_PREFIX).strip()
