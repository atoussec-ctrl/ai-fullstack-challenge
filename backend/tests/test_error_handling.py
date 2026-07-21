"""TDD: central error handlers map typed exceptions to the right HTTP status.

Replaces the previous pattern where every route decided ad hoc whether a bare
ValueError meant "invalid input" (400) or "resource not found" (404).
"""

from __future__ import annotations

from app.errors import NotFoundError, ValidationError


def test_not_found_error_maps_to_404_json_envelope(app, client):
    @app.route("/__test/not-found")
    def _raise_not_found():
        raise NotFoundError("Recurso não encontrado.")

    response = client.get("/__test/not-found")

    assert response.status_code == 404
    body = response.get_json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["message"] == "Recurso não encontrado."


def test_validation_error_maps_to_400_json_envelope_with_field(app, client):
    @app.route("/__test/validation")
    def _raise_validation():
        raise ValidationError("Campo obrigatório.", field="title")

    response = client.get("/__test/validation")

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Campo obrigatório."
    assert body["error"]["details"]["field"] == "title"


def test_validation_error_without_field_omits_details_field(app, client):
    @app.route("/__test/validation-no-field")
    def _raise_validation():
        raise ValidationError("Entrada inválida.")

    response = client.get("/__test/validation-no-field")

    assert response.status_code == 400
    assert response.get_json()["error"]["details"] == {}


def test_validation_error_is_a_value_error_for_backward_compatible_catches():
    """Existing call sites doing `except ValueError` must keep catching it."""
    assert isinstance(ValidationError("x"), ValueError)


def test_not_found_error_is_not_a_value_error():
    """Not-found must NOT be swallowed by a generic `except ValueError` 400 path."""
    assert not isinstance(NotFoundError("x"), ValueError)
