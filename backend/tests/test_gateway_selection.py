"""TDD para MS-106: DeepSeek V4 via Hugging Face Inference API, mantendo OpenAI."""

from __future__ import annotations

from app.services.chat import (
    HF_ROUTER_BASE_URL,
    LangChainOpenAIGateway,
    LocalPythonAssistantGateway,
    build_chat_gateway,
    chat_model_kwargs,
)


def _set(app, **overrides):
    defaults = {
        "CHAT_GATEWAY": "auto",
        "OPENAI_API_KEY": "",
        "HUGGINGFACE_API_KEY": "",
        "HF_CHAT_MODEL": "deepseek-ai/DeepSeek-V4-Flash",
        "HF_BASE_URL": HF_ROUTER_BASE_URL,
    }
    defaults.update(overrides)
    app.config.update(defaults)


# ── chat_model_kwargs por família de modelo ──


def test_deepseek_kwargs_use_official_recommendation():
    kwargs = chat_model_kwargs("deepseek-ai/DeepSeek-V4-Flash", "deep")
    assert kwargs == {"temperature": 1.0}


def test_openai_kwargs_keep_current_behavior():
    assert chat_model_kwargs("gpt-4.1-mini", "balanced") == {"temperature": 0.3}
    assert chat_model_kwargs("o3-mini", "deep") == {"reasoning_effort": "high"}


# ── Seleção de gateway ──


def test_huggingface_mode_builds_router_gateway(app):
    with app.app_context():
        _set(app, CHAT_GATEWAY="huggingface", HUGGINGFACE_API_KEY="hf_test")
        gateway = build_chat_gateway()

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "deepseek-ai/DeepSeek-V4-Flash"
        assert gateway.base_url == HF_ROUTER_BASE_URL
        assert gateway.api_key == "hf_test"


def test_auto_prefers_huggingface_over_openai(app):
    with app.app_context():
        _set(app, HUGGINGFACE_API_KEY="hf_test", OPENAI_API_KEY="sk-test")
        gateway = build_chat_gateway()

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.base_url == HF_ROUTER_BASE_URL


def test_auto_without_any_key_falls_back_to_local(app):
    with app.app_context():
        _set(app)
        assert isinstance(build_chat_gateway(), LocalPythonAssistantGateway)


def test_explicit_openai_model_keeps_openai_gateway(app):
    with app.app_context():
        _set(app, HUGGINGFACE_API_KEY="hf_test", OPENAI_API_KEY="sk-test")
        gateway = build_chat_gateway("gpt-4.1")

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "gpt-4.1"
        assert gateway.base_url is None
        assert gateway.api_key == "sk-test"


def test_explicit_deepseek_model_routes_to_huggingface(app):
    with app.app_context():
        _set(app, HUGGINGFACE_API_KEY="hf_test", OPENAI_API_KEY="sk-test", CHAT_GATEWAY="openai")
        gateway = build_chat_gateway("deepseek-ai/DeepSeek-V4-Pro")

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "deepseek-ai/DeepSeek-V4-Pro"
        assert gateway.base_url == HF_ROUTER_BASE_URL


def test_huggingface_mode_without_key_raises(app):
    with app.app_context():
        _set(app, CHAT_GATEWAY="huggingface")
        try:
            build_chat_gateway()
            raise AssertionError("deveria ter levantado ValueError")
        except ValueError as exc:
            assert "HUGGINGFACE_API_KEY" in str(exc)
