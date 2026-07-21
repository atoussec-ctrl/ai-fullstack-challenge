"""TDD para MS-106: DeepSeek V4 via Hugging Face Inference API, mantendo OpenAI."""

from __future__ import annotations

from app.services.chat import (
    HF_ROUTER_BASE_URL,
    LangChainOpenAIGateway,
    LocalPythonAssistantGateway,
    build_chat_gateway,
    chat_max_output_tokens,
    chat_model_kwargs,
    extract_ai_message_content,
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


def test_deepseek_kwargs_use_official_recommendation(app):
    with app.app_context():
        kwargs = chat_model_kwargs("deepseek-ai/DeepSeek-V4-Flash", "deep")
    assert kwargs == {"max_tokens": 4096, "temperature": 1.0}


def test_openai_kwargs_keep_current_behavior(app):
    with app.app_context():
        assert chat_model_kwargs("gpt-4.1-mini", "balanced") == {
            "max_tokens": 4096,
            "temperature": 0.3,
        }
        assert chat_model_kwargs("o3-mini", "deep") == {
            "max_tokens": 4096,
            "reasoning_effort": "high",
        }


def test_chat_max_output_tokens_reads_from_config(app):
    with app.app_context():
        app.config["CHAT_MAX_OUTPUT_TOKENS"] = 8192
        assert chat_max_output_tokens() == 8192


def test_extract_ai_message_content_supports_block_lists():
    class FakeResponse:
        content = [{"type": "text", "text": "Olá "}, {"type": "text", "text": "mundo"}]

    assert extract_ai_message_content(FakeResponse()) == "Olá mundo"


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


def test_auto_ignores_placeholder_keys_from_env_example(app):
    with app.app_context():
        _set(
            app,
            OPENAI_API_KEY="replace-me",
            HUGGINGFACE_API_KEY="replace-me",
        )
        assert isinstance(build_chat_gateway(), LocalPythonAssistantGateway)


def test_explicit_openai_model_keeps_openai_gateway(app):
    with app.app_context():
        _set(
            app,
            HUGGINGFACE_API_KEY="hf_test",
            OPENAI_API_KEY="sk-test",
            ALLOWED_CHAT_MODELS="gpt-4.1",
        )
        gateway = build_chat_gateway("gpt-4.1")

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "gpt-4.1"
        assert gateway.base_url is None
        assert gateway.api_key == "sk-test"


def test_explicit_deepseek_model_routes_to_huggingface(app):
    with app.app_context():
        _set(
            app,
            HUGGINGFACE_API_KEY="hf_test",
            OPENAI_API_KEY="sk-test",
            CHAT_GATEWAY="openai",
            ALLOWED_CHAT_MODELS="deepseek-ai/DeepSeek-V4-Pro",
        )
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


# ── Allowlist de modelo (MS-security: impede abuso de custo via modelo arbitrário) ──


def test_client_requested_model_outside_allowlist_is_rejected(app):
    with app.app_context():
        _set(app, HUGGINGFACE_API_KEY="hf_test", OPENAI_API_KEY="sk-test")
        try:
            build_chat_gateway("some-arbitrary-expensive-model")
            raise AssertionError("deveria ter levantado ValidationError")
        except ValueError as exc:
            assert "não está na lista de modelos permitidos" in str(exc)


def test_default_allowlist_permits_the_operators_own_configured_models(app):
    """Without ALLOWED_CHAT_MODELS, only the operator's own defaults are usable."""
    with app.app_context():
        _set(
            app,
            HUGGINGFACE_API_KEY="hf_test",
            OPENAI_API_KEY="sk-test",
            HF_CHAT_MODEL="deepseek-ai/DeepSeek-V4-Flash",
        )
        gateway = build_chat_gateway("deepseek-ai/DeepSeek-V4-Flash")

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "deepseek-ai/DeepSeek-V4-Flash"


def test_explicit_allowlist_permits_extra_models(app):
    with app.app_context():
        _set(
            app,
            HUGGINGFACE_API_KEY="hf_test",
            OPENAI_API_KEY="sk-test",
            ALLOWED_CHAT_MODELS="deepseek-ai/DeepSeek-V4-Flash, deepseek-ai/DeepSeek-V4-Pro",
        )
        gateway = build_chat_gateway("deepseek-ai/DeepSeek-V4-Pro")

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.model == "deepseek-ai/DeepSeek-V4-Pro"
