"""Unit tests for pure helpers in app.config not exercised by the app fixture.

TestingConfig hardcodes SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:"
directly, so resolve_sqlite_url's relative-path branches (used by
Development/ProductionConfig via DATABASE_URL) are otherwise never run.
"""

from __future__ import annotations

import pytest

from app.config import (
    BASE_DIR,
    InsecureConfigurationError,
    assert_production_config_is_safe,
    resolve_sqlite_url,
)


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


@pytest.mark.parametrize(
    "secret_key",
    ["", "replace-me", "changeme", "change-me", "dev-secret-key-change-me"],
)
def test_assert_production_config_rejects_placeholder_secret_key(secret_key):
    with pytest.raises(InsecureConfigurationError, match="SECRET_KEY"):
        assert_production_config_is_safe({"SECRET_KEY": secret_key, "API_KEY": "a-real-key"})


@pytest.mark.parametrize("api_key", ["", "replace-me", "changeme", "change-me"])
def test_assert_production_config_rejects_placeholder_api_key(api_key):
    with pytest.raises(InsecureConfigurationError, match="API_KEY"):
        assert_production_config_is_safe({"SECRET_KEY": "a-real-secret", "API_KEY": api_key})


def test_assert_production_config_accepts_real_secrets():
    assert_production_config_is_safe({"SECRET_KEY": "a-real-secret", "API_KEY": "a-real-key"})
