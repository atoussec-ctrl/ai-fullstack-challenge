# Status de Implementação

Data: 2026-06-12

## Backend

Implementado em Flask com SQLite e testes automatizados.

### Endpoints disponíveis

- `GET /health`
- `GET /api/v1/health`
- `POST /api/v1/books`
- `POST /api/v1/books/import`
- `GET /api/v1/books?title=&author=`
- `GET /api/v1/books?q=`
- `GET /api/v1/chat/sessions`
- `POST /api/v1/chat/sessions`
- `PATCH /api/v1/chat/sessions/{session_id}` — fixar/desafixar
- `DELETE /api/v1/chat/sessions/{session_id}`
- `GET /api/v1/chat/sessions/{session_id}/messages`
- `POST /api/v1/chat/messages`
- `GET /api/v1/chat/messages/{assistant_message_id}/stream`
- `POST /api/v1/chat/messages/{assistant_message_id}/feedback`
- `POST /api/v1/attachments`
- `GET /api/v1/attachments/{attachment_id}`
- `POST /api/v1/semantic-search`
- `GET /openapi.json`
- `GET /docs`

### Arquitetura

- Modelos SQLAlchemy: `Book`, `ChatSession`, `ChatMessage`, `Attachment`.
- Repositórios para persistência de livros e chat.
- Serviços para livros, importação assistida por upload, chat, upload e busca semântica.
- Gateway de IA fakeável em testes e desenvolvimento local (`CHAT_GATEWAY=local`).
- Gateway LangChain/OpenAI opcional; placeholders de `.env.example` são ignorados.
- Chat usa a biblioteca local como contexto quando a pergunta menciona livros cadastrados.
- LangSmith opcional por `LANGSMITH_TRACING=true`.
- Sessões fixáveis (`pinned`, `pinned_at`) com ordenação na sidebar.
- Busca semântica MVP com embeddings locais determinísticos para CI.

### Dependências

- `backend/requirements.txt`: runtime core e ferramentas de teste.
- `backend/requirements-ai.txt`: integrações opcionais LangChain/OpenAI/FAISS.
- Instalação via `make install` (venv em `backend/.venv`).

## Frontend

Implementado em Vite + React + TypeScript com TanStack Query, Tailwind CSS, Framer Motion e lucide-react.

### Funcionalidades disponíveis

- Layout de chat responsivo com sidebar desktop e drawer mobile.
- Tela de administração e consulta de livros (grid/carrossel, filtros).
- Cadastro manual e importação de livros por upload.
- Histórico de conversas, pin/unpin e exclusão (swipe no mobile).
- Composer com reset imediato, indicador "Pensando" e botão parar.
- Modos de raciocínio: `fast`, `balanced`, `deep`.
- Tema claro/escuro, uploads e gravação de áudio.
- Markdown com blocos de código e feedback "Copiado!".

## Onboarding e documentação

- [`README.md`](../README.md): Quick Start, pré-requisitos, troubleshooting.
- [`.env.example`](../.env.example): defaults `CHAT_GATEWAY=local` e chaves vazias.
- [`Makefile`](../Makefile): fallback de venv quando `python3-venv` não está instalado.

## Testes e checks executados

### Backend

```bash
make backend-test
make lint
```

Resultado: **41 testes** passando (pytest).

### Frontend

```bash
make frontend-test
make lint
make typecheck
make build
cd frontend && pnpm test:e2e
```

Resultado: **43 testes** unitários (Vitest), lint/typecheck/build OK.
E2E Playwright: **5 passando**, **1 pulado** (mobile-only).

## Observações

- Frontend na porta **3002** (`strictPort` no Vite).
- Docker Compose exige `.env` na raiz e portas 5000/3002 livres.
- Playwright usa `channel: chrome` (Google Chrome do sistema).
