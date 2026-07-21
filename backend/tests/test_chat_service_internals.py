"""Unit tests closing coverage gaps in app.services.chat.

Covers the LangChainOpenAIGateway body (mocking ChatOpenAI so no real network
call happens — the same technique already used for langsmith.Client in
test_feedback_resilience.py), plus gateway-selection branches and small
defensive paths not reached by the HTTP-level test suites.
"""

from __future__ import annotations

import logging
from datetime import date

import pytest

from app.errors import NotFoundError
from app.extensions import db
from app.models import Attachment, Book
from app.repositories import ChatRepository
from app.services.chat import (
    DEFAULT_CHAT_GATEWAY_TIMEOUT_SECONDS,
    DEFAULT_CHAT_MAX_MESSAGE_CHARS,
    DEFAULT_CHAT_MAX_OUTPUT_TOKENS,
    HF_ROUTER_BASE_URL,
    ChatCompletionGateway,
    ChatService,
    LangChainOpenAIGateway,
    _effective_api_key,
    build_chat_gateway,
    chat_gateway_timeout_seconds,
    chat_max_message_chars,
    chat_max_output_tokens,
    extract_ai_message_content,
    format_attachment_context,
    normalize_thinking_mode,
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


# ── ChatCompletionGateway: interface abstrata ──


def test_chat_completion_gateway_base_class_is_not_implemented():
    with pytest.raises(NotImplementedError):
        ChatCompletionGateway().answer("pergunta", "fast")


# ── LangChainOpenAIGateway.answer(): corpo real, ChatOpenAI mockado ──


def test_langchain_gateway_builds_prompt_and_returns_content(app, monkeypatch):
    import langchain_openai

    captured: dict[str, object] = {}

    class FakeResponse:
        content = "Resposta gerada pelo modelo."
        response_metadata = {"finish_reason": "stop"}

    class FakeChatOpenAI:
        def __init__(self, **kwargs):
            captured["kwargs"] = kwargs

        def invoke(self, messages):
            captured["messages"] = messages
            return FakeResponse()

    monkeypatch.setattr(langchain_openai, "ChatOpenAI", FakeChatOpenAI)

    book = Book(
        id="book-1",
        title="Clean Architecture",
        category="Engenharia",
        author="Robert Martin",
        publication_date=date(2017, 1, 1),
        summary="Princípios de arquitetura de software.",
    )

    with app.app_context():
        gateway = LangChainOpenAIGateway(model="gpt-4.1-mini", api_key="sk-test")
        result = gateway.answer(
            "O que é uma lista?",
            "balanced",
            book_context=[book],
            history=[{"role": "user", "content": "oi"}, {"role": "assistant", "content": "olá"}],
            attachment_context="Anexo: notas.txt\nConteúdo:\nfoo",
        )

    assert result == "Resposta gerada pelo modelo."
    assert captured["kwargs"]["model"] == "gpt-4.1-mini"
    # system + histórico (2 turnos) + turno atual do usuário
    assert len(captured["messages"]) == 4
    assert captured["kwargs"]["timeout"] == DEFAULT_CHAT_GATEWAY_TIMEOUT_SECONDS


def test_langchain_gateway_uses_configured_timeout(app, monkeypatch):
    import langchain_openai

    captured: dict[str, object] = {}

    class FakeResponse:
        content = "ok"
        response_metadata = {"finish_reason": "stop"}

    class FakeChatOpenAI:
        def __init__(self, **kwargs):
            captured["kwargs"] = kwargs

        def invoke(self, messages):
            return FakeResponse()

    monkeypatch.setattr(langchain_openai, "ChatOpenAI", FakeChatOpenAI)

    with app.app_context():
        app.config["CHAT_GATEWAY_TIMEOUT_SECONDS"] = 5
        gateway = LangChainOpenAIGateway(model="gpt-4.1-mini", api_key="sk-test")
        gateway.answer("pergunta", "fast")

    assert captured["kwargs"]["timeout"] == 5


def test_langchain_gateway_appends_truncation_notice_when_length_limited(app, monkeypatch):
    import langchain_openai

    class FakeResponse:
        content = "Resposta cortada no meio"
        response_metadata = {"finish_reason": "length"}

    class FakeChatOpenAI:
        def __init__(self, **kwargs):
            pass

        def invoke(self, messages):
            return FakeResponse()

    monkeypatch.setattr(langchain_openai, "ChatOpenAI", FakeChatOpenAI)

    with app.app_context():
        gateway = LangChainOpenAIGateway(model="gpt-4.1-mini", api_key="sk-test")
        result = gateway.answer("pergunta", "fast")

    assert "Resposta cortada no meio" in result
    assert "interrompida por limite de tokens" in result


# ── extract_ai_message_content: ramos de bloco de conteúdo ──


def test_extract_ai_message_content_supports_plain_string_blocks():
    class FakeResponse:
        content = ["Olá ", "mundo"]

    assert extract_ai_message_content(FakeResponse()) == "Olá mundo"


def test_extract_ai_message_content_falls_back_to_str_for_unknown_shapes():
    class FakeResponse:
        content = 12345

    assert extract_ai_message_content(FakeResponse()) == "12345"


# ── Configuração fora de contexto de aplicação ──


def test_chat_max_output_tokens_reads_os_environ_without_app_context(monkeypatch):
    monkeypatch.setenv("CHAT_MAX_OUTPUT_TOKENS", "2048")

    assert chat_max_output_tokens() == 2048


def test_chat_max_output_tokens_falls_back_to_default_when_not_numeric(app):
    with app.app_context():
        app.config["CHAT_MAX_OUTPUT_TOKENS"] = "não-é-um-número"

        assert chat_max_output_tokens() == DEFAULT_CHAT_MAX_OUTPUT_TOKENS


def test_chat_max_message_chars_falls_back_to_default_when_not_numeric(app):
    with app.app_context():
        app.config["CHAT_MAX_MESSAGE_CHARS"] = "não-é-um-número"

        assert chat_max_message_chars() == DEFAULT_CHAT_MAX_MESSAGE_CHARS


# ── chat_gateway_timeout_seconds ──


def test_chat_gateway_timeout_seconds_reads_from_config(app):
    with app.app_context():
        app.config["CHAT_GATEWAY_TIMEOUT_SECONDS"] = 45
        assert chat_gateway_timeout_seconds() == 45


def test_chat_gateway_timeout_seconds_falls_back_to_default_when_not_numeric(app):
    with app.app_context():
        app.config["CHAT_GATEWAY_TIMEOUT_SECONDS"] = "não-é-um-número"
        assert chat_gateway_timeout_seconds() == DEFAULT_CHAT_GATEWAY_TIMEOUT_SECONDS


def test_chat_gateway_timeout_seconds_is_clamped_to_a_sane_upper_bound(app):
    with app.app_context():
        app.config["CHAT_GATEWAY_TIMEOUT_SECONDS"] = 10_000
        assert chat_gateway_timeout_seconds() == 300


def test_chat_gateway_timeout_seconds_is_clamped_to_a_sane_lower_bound(app):
    with app.app_context():
        app.config["CHAT_GATEWAY_TIMEOUT_SECONDS"] = 0
        assert chat_gateway_timeout_seconds() == 1


# ── build_chat_gateway: ramos de seleção não cobertos pelos testes existentes ──


def test_auto_mode_with_hub_model_and_no_hf_key_falls_back_to_local(app):
    with app.app_context():
        _set(app)  # auto, sem chaves
        from app.services.chat import LocalPythonAssistantGateway

        gateway = build_chat_gateway("deepseek-ai/DeepSeek-V4-Flash")

        assert isinstance(gateway, LocalPythonAssistantGateway)


def test_openai_mode_without_key_raises(app):
    with app.app_context():
        _set(app, CHAT_GATEWAY="openai")
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            build_chat_gateway()


def test_auto_mode_without_hf_key_falls_back_to_openai(app):
    with app.app_context():
        _set(app, OPENAI_API_KEY="sk-test")
        gateway = build_chat_gateway()

        assert isinstance(gateway, LangChainOpenAIGateway)
        assert gateway.base_url is None


# ── _effective_api_key: placeholders com prefixo "replace-" fora da lista exata ──


def test_effective_api_key_rejects_any_replace_prefixed_placeholder():
    assert _effective_api_key("replace-with-your-own-token") == ""


# ── normalize_thinking_mode: default quando vazio ──


def test_normalize_thinking_mode_defaults_to_balanced_when_empty():
    assert normalize_thinking_mode(None) == "balanced"
    assert normalize_thinking_mode("") == "balanced"


# ── ChatService.ask(): unit of work — tudo ou nada ──


def test_ask_is_atomic_nothing_persists_if_the_final_commit_fails(app, monkeypatch):
    """Regression guard for the single-commit unit of work.

    Before this refactor, create_message/attach_to_message each committed
    independently — a failure at the very end still left the user message
    (and any attached files) permanently persisted. Now everything is only
    flushed until one commit at the end of ask(), so a failure there must
    roll back the whole exchange, not leave a half-written conversation.
    """

    class RecordingGateway(ChatCompletionGateway):
        def answer(self, *args, **kwargs):
            return "resposta"

    with app.app_context():
        service = ChatService(gateway=RecordingGateway())
        session = service.create_session("atomicidade")

        def failing_commit():
            raise RuntimeError("falha simulada no commit final")

        monkeypatch.setattr(db.session, "commit", failing_commit)

        with pytest.raises(RuntimeError, match="falha simulada"):
            service.ask(session_id=session.id, content="oi", thinking_mode="fast")

        monkeypatch.undo()  # restore the real commit for the assertions below
        db.session.rollback()  # clear the failed transaction

        assert ChatRepository().list_messages(session.id) == []


# ── ChatService.delete_session: ramos defensivos ──


def test_delete_session_raises_when_repository_delete_fails_after_existence_check(app):
    class FlakyRepository(ChatRepository):
        def delete_session(self, session_id: str) -> bool:
            return False  # simula falha mesmo com a sessão existindo

    with app.app_context():
        repository = FlakyRepository()
        service = ChatService(repository=repository)
        session = service.create_session("efêmera")

        with pytest.raises(NotFoundError):
            service.delete_session(session.id)


def test_delete_session_logs_warning_when_attachment_cleanup_fails(app, tmp_path, caplog):
    with app.app_context():
        repository = ChatRepository()
        session = repository.create_session("com anexo problemático")
        attachment = Attachment(
            session_id=session.id,
            filename="pasta",
            mime_type="application/octet-stream",
            size=0,
            kind="document",
            storage_path=str(tmp_path),  # diretório, não arquivo -> unlink() levanta OSError
        )
        db.session.add(attachment)
        db.session.commit()

        with caplog.at_level(logging.WARNING):
            ChatService(repository=repository).delete_session(session.id)

        assert "Não foi possível remover anexo" in caplog.text


# ── format_attachment_context: texto não extraível ──


def test_format_attachment_context_notes_when_text_extraction_unavailable():
    attachment = Attachment(
        session_id="s1",
        filename="foto.png",
        mime_type="image/png",
        size=10,
        kind="image",
        storage_path="/nao-existe/foto.png",
    )

    context = format_attachment_context([attachment])

    assert context is not None
    assert "sem extração de texto disponível" in context
