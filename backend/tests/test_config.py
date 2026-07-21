"""Unit tests for pure helpers in app.config not exercised by the app fixture.

TestingConfig hardcodes SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:"
directly, so resolve_sqlite_url's relative-path branches (used by
Development/ProductionConfig via DATABASE_URL) are otherwise never run.
"""

from __future__ import annotations

from app.config import BASE_DIR, resolve_sqlite_url


def test_resolve_sqlite_url_converts_dot_relative_path():
    result = resolve_sqlite_url("sqlite:///./storage/app.db")

    assert result == f"sqlite:///{BASE_DIR / 'storage/app.db'}"


def test_resolve_sqlite_url_converts_bare_relative_path():
    result = resolve_sqlite_url("sqlite:///storage/app.db")

    assert result == f"sqlite:///{BASE_DIR / 'storage/app.db'}"


def test_resolve_sqlite_url_leaves_absolute_four_slash_path_untouched():
    result = resolve_sqlite_url("sqlite:////absolute/path/app.db")

    assert result == "sqlite:////absolute/path/app.db"


def test_resolve_sqlite_url_leaves_non_sqlite_urls_untouched():
    result = resolve_sqlite_url("postgresql://user:pass@localhost/db")

    assert result == "postgresql://user:pass@localhost/db"
