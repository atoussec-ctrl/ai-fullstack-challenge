"""Tests for repository-root .env loading and LangSmith env normalization."""

from __future__ import annotations

import os
from pathlib import Path

from app.env_loader import ENV_FILE, PROJECT_ROOT, load_project_env


def test_project_root_points_to_repository_root():
    assert PROJECT_ROOT.name == "mindsight"
    assert ENV_FILE == PROJECT_ROOT / ".env"


def test_load_project_env_normalizes_placeholder_langsmith_key(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "LANGSMITH_TRACING=true",
                "LANGSMITH_API_KEY=replace-me",
                "LANGCHAIN_API_KEY=lsv2_test_key",
                "LANGSMITH_PROJECT=mindsight-ai",
            ]
        )
        + "\n"
    )

    monkeypatch.setattr("app.env_loader.ENV_FILE", env_file)
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    monkeypatch.delenv("LANGCHAIN_TRACING_V2", raising=False)

    loaded = load_project_env()

    assert loaded == env_file
    assert os.environ["LANGSMITH_API_KEY"] == "lsv2_test_key"
    assert os.environ["LANGCHAIN_TRACING_V2"] == "true"


def test_load_project_env_keeps_real_langsmith_key(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "LANGSMITH_API_KEY=lsv2_real\nLANGCHAIN_API_KEY=lsv2_legacy\n"
    )

    monkeypatch.setattr("app.env_loader.ENV_FILE", env_file)
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)

    load_project_env()

    assert os.environ["LANGSMITH_API_KEY"] == "lsv2_real"
