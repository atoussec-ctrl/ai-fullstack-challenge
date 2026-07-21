"""Typed application exceptions.

A bare ValueError used to mean both "invalid input" (400) and "resource not
found" (404), interpreted differently ad hoc at each call site. These types
remove the ambiguity: raise the one that matches the situation and let the
central handlers (see app/__init__.py) pick the right status code.

ValidationError subclasses ValueError on purpose so existing `except
ValueError` call sites keep working unchanged during the migration.
NotFoundError does NOT subclass ValueError — a missing resource must never be
silently swallowed by a generic "invalid input" handler.
"""

from __future__ import annotations


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""


class ValidationError(ValueError):
    """Raised when request input fails validation."""

    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field
