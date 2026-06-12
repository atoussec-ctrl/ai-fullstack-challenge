"""Chat use cases and AI gateway abstractions."""

from __future__ import annotations

from dataclasses import dataclass

from flask import current_app, has_app_context

from app.models import Book
from app.repositories import BookRepository, ChatRepository
from app.services.observability import current_run_id, traceable_if_enabled

SYSTEM_PROMPT = """Você é um assistente sênior especializado em Python.
Responda em português.
Explique passo a passo quando necessário.
Inclua exemplos de código claros.
Quando houver risco de erro, avise.
Não invente APIs.
Priorize Flask, FastAPI, SQLAlchemy, testes, arquitetura e boas práticas."""

THINKING_MODES: dict[str, dict[str, object]] = {
    "fast": {
        "temperature": 0.2,
        "reasoning_effort": "low",
        "instruction": "Seja direto e objetivo.",
    },
    "balanced": {
        "temperature": 0.3,
        "reasoning_effort": "medium",
        "instruction": "Explique com exemplos.",
    },
    "deep": {
        "temperature": 0.2,
        "reasoning_effort": "high",
        "instruction": "Analise trade-offs e detalhe.",
    },
}


@dataclass(frozen=True)
class ChatAnswer:
    content: str
    thinking_mode: str


class ChatCompletionGateway:
    def answer(
        self,
        question: str,
        thinking_mode: str,
        book_context: list[Book] | None = None,
    ) -> str:
        raise NotImplementedError


class LocalPythonAssistantGateway(ChatCompletionGateway):
    """Deterministic local gateway for development and tests."""

    @traceable_if_enabled("chat.local_python_assistant", run_type="llm")
    def answer(
        self,
        question: str,
        thinking_mode: str,
        book_context: list[Book] | None = None,
    ) -> str:
        normalized = question.strip().lower()
        mode_hint = THINKING_MODES[thinking_mode]["instruction"]
        if book_context:
            book_lines = []
            for book in book_context:
                book_lines.append(
                    "\n".join(
                        [
                            f"- Título: {book.title}",
                            f"  Categoria: {book.category}",
                            f"  Autor: {book.author}",
                            f"  Publicação: {book.publication_date.isoformat()}",
                            f"  Resumo: {book.summary}",
                            f"  Fonte: biblioteca local, id `{book.id}`",
                        ]
                    )
                )
            return (
                "Encontrei informações na biblioteca local e vou citar apenas o que "
                "está registrado na base.\n\n"
                f"{chr(10).join(book_lines)}\n\n"
                "Com base nesses registros, posso resumir, explicar trechos do resumo "
                "e comparar os livros encontrados. Se você pedir algo que não esteja "
                "nesses campos, eu vou sinalizar a limitação em vez de inventar. "
                f"Modo de resposta: {thinking_mode}. {mode_hint}"
            )
        if "lista" in normalized:
            return (
                "Em Python, uma lista é criada usando colchetes.\n\n"
                "```python\n"
                "numbers = [1, 2, 3]\n"
                "names = [\"Ana\", \"Bruno\", \"Carla\"]\n"
                "names.append(\"Daniel\")\n"
                "print(names[0])\n"
                "```\n\n"
                "Listas preservam ordem, aceitam itens repetidos e são mutáveis. "
                f"Modo de resposta: {thinking_mode}. {mode_hint}"
            )
        return (
            "Posso ajudar com Python, Flask, SQLAlchemy, testes e arquitetura. "
            "Envie o trecho de código, erro ou objetivo, e eu respondo em português "
            f"com foco prático. Modo de resposta: {thinking_mode}. {mode_hint}"
        )


class LangChainOpenAIGateway(ChatCompletionGateway):
    """Optional production gateway. Imported lazily so tests do not require LangChain."""

    def __init__(self, model: str, api_key: str) -> None:
        self.model = model
        self.api_key = api_key

    @traceable_if_enabled("chat.langchain_openai", run_type="llm")
    def answer(
        self,
        question: str,
        thinking_mode: str,
        book_context: list[Book] | None = None,
    ) -> str:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI
        except ImportError as exc:  # pragma: no cover - depends on optional packages
            raise RuntimeError("Dependências LangChain/OpenAI não instaladas.") from exc

        mode = THINKING_MODES[thinking_mode]
        llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=float(mode["temperature"]),
            reasoning_effort=str(mode["reasoning_effort"]),
        )
        book_context_text = format_book_context(book_context or [])
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        f"{SYSTEM_PROMPT}\n{mode['instruction']}\n"
                        "Quando houver contexto de livros, cite somente dados presentes "
                        "na biblioteca local e informe a fonte/id."
                    )
                ),
                HumanMessage(content=f"{book_context_text}\n\nPergunta: {question}"),
            ]
        )
        return str(response.content)


def build_chat_gateway(model: str | None = None) -> ChatCompletionGateway:
    if has_app_context():
        gateway_mode = str(current_app.config.get("CHAT_GATEWAY", "local")).lower()
        api_key = str(current_app.config.get("OPENAI_API_KEY", ""))
        default_model = str(current_app.config.get("OPENAI_MODEL", "gpt-4.1-mini"))
    else:
        import os

        gateway_mode = os.getenv("CHAT_GATEWAY", "local").lower()
        api_key = os.getenv("OPENAI_API_KEY", "")
        default_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if gateway_mode not in {"local", "auto", "openai"}:
        raise ValueError("CHAT_GATEWAY deve ser local, auto ou openai.")
    if gateway_mode == "local":
        return LocalPythonAssistantGateway()
    if not api_key:
        if gateway_mode == "auto":
            return LocalPythonAssistantGateway()
        raise ValueError("OPENAI_API_KEY é obrigatório quando CHAT_GATEWAY=openai.")
    return LangChainOpenAIGateway(model=(model or default_model), api_key=api_key)


def normalize_thinking_mode(value: str | None) -> str:
    if not value:
        return "balanced"
    normalized = value.strip().lower()
    if normalized not in THINKING_MODES:
        raise ValueError("thinking_mode deve ser fast, balanced ou deep.")
    return normalized


class ChatService:
    def __init__(
        self,
        repository: ChatRepository | None = None,
        gateway: ChatCompletionGateway | None = None,
        book_repository: BookRepository | None = None,
        model: str | None = None,
    ) -> None:
        self.repository = repository or ChatRepository()
        self.gateway = gateway or build_chat_gateway(model)
        self.book_repository = book_repository or BookRepository()

    def create_session(self, title: str = "Nova conversa"):
        return self.repository.create_session(title)

    @traceable_if_enabled("chat.ask", run_type="chain")
    def ask(
        self,
        *,
        session_id: str,
        content: str,
        thinking_mode: str | None,
        attachment_ids: list[str] | None = None,
    ) -> tuple[object, object]:
        if not self.repository.get_session(session_id):
            raise ValueError("Sessão de chat não encontrada.")
        if not content.strip() and not attachment_ids:
            raise ValueError("Campo content é obrigatório quando não há anexos.")

        mode = normalize_thinking_mode(thinking_mode)
        user_message = self.repository.create_message(
            session_id=session_id,
            role="user",
            content=content.strip(),
            thinking_mode=mode,
        )
        if attachment_ids:
            self.repository.attach_to_message(attachment_ids, user_message.id)

        book_context = self.book_repository.relevant_for_question(content)
        answer = self.gateway.answer(content, mode, book_context=book_context)
        trace_id = current_run_id()
        assistant_message = self.repository.create_message(
            session_id=session_id,
            role="assistant",
            content=answer,
            thinking_mode=mode,
            status="completed",
            trace_id=trace_id,
        )
        return user_message, assistant_message


def format_book_context(books: list[Book]) -> str:
    if not books:
        return "Contexto de livros: nenhum livro relevante encontrado na biblioteca local."
    blocks = [
        "\n".join(
            [
                f"Livro id: {book.id}",
                f"Título: {book.title}",
                f"Categoria: {book.category}",
                f"Autor: {book.author}",
                f"Data de publicação: {book.publication_date.isoformat()}",
                f"Resumo: {book.summary}",
            ]
        )
        for book in books
    ]
    return "Contexto de livros da biblioteca local:\n\n" + "\n\n".join(blocks)
