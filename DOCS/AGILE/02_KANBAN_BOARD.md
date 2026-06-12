# Kanban Board — MindSight AI

Colunas: **Backlog → Ready → In Progress → Review/QA → Done**
Política: WIP limit 2/pessoa em In Progress; item só entra em Ready com DoR completo; só sai de Review/QA com DoD completo.

## Estado atual do board

### 📋 Backlog

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| MS-104 | Importação de livro com LLM real | `ai` `feature` | P2 | 5 |
| MS-203 | UI de busca semântica | `frontend` `feature` | P2 | 3 |
| MS-302 | Hardening de produção | `security` `infra` | P2 | 5 |
| MS-402 | Métricas Prometheus | `observability` `backend` | P2 | 5 |
| MS-403 | Feedback LangSmith na UI | `frontend` `observability` | P2 | 3 |
| MS-602 | Vazamentos de camada no backend | `refactor` `backend` | P2 | 3 |
| MS-005 | Remover dependências mortas | `refactor` | P2 | 2 |

### ✅ Ready (DoR completo — próxima sprint)

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| MS-008 | Migrations versionadas (Flask-Migrate/Alembic) | `infra` `backend` `refactor` | P1 | 5 |
| MS-006 | Pipeline CI com quality gates | `infra` `testing` | P1 | 5 |
| MS-103 | Streaming SSE real do LLM | `ai` `feature` `backend` | P1 | 8 |
| MS-603 | Streaming consumido na UI | `frontend` `feature` | P1 | 5 |

### 🔨 In Progress

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| — | *(vazio)* | | | |

### 🔍 Review/QA

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| — | *(vazio)* | | | |

### ✔️ Done — Sprint 1.1 — fixes do Bugbot + infra (2026-06-12)

| Card | Título | Labels |
|---|---|---|
| MS-604 | Retry deixa de duplicar sessões no frontend (F-30) — teste de regressão Vitest | `bug` `frontend` |
| MS-105 | Extração real de texto de PDF (pypdf) no import e em anexos do chat (F-29) | `bug` `backend` |
| MS-007 | Build do Docker Compose corrigido (pnpm v11 allowBuilds + COPY do workspace) (F-31) | `bug` `infra` `frontend` |
| MS-009 | Seed idempotente + backup/restore do SQLite (preserva dados ao atualizar UI) | `infra` `backend` |
| MS-106 | DeepSeek V4 via HF Inference API mantendo OpenAI — validado ao vivo (F-33 fix incluso) | `ai` `feature` `backend` `frontend` |

### ✔️ Done — Sprint 1 (2026-06-11)

| Card | Título | Labels |
|---|---|---|
| MS-001 | Primeiro commit + DOCS fora do .gitignore | `infra` `docs` |
| MS-003 | Lint zero + gate de cobertura no Makefile | `testing` `backend` |
| MS-004 | Sanear .env (CHAT_GATEWAY, SECRET_KEY, HF key órfã removida) | `security` `infra` |
| MS-101 | Histórico multi-turn (TDD: 8 novos testes) | `ai` `feature` `backend` |
| MS-102 | Anexos como contexto da IA + validação de sessão (F-26/27/28) | `ai` `feature` `backend` |

### ✔️ Done (entregue até a auditoria de 2026-06-11)

| Card | Título | Labels |
|---|---|---|
| BE | API Flask de livros (CRUD + busca título/autor/categoria/q) com SQLite | `backend` `feature` |
| BE | Chat com sessões, mensagens, gateway local + LangChain/OpenAI opcional | `ai` `backend` |
| BE | Upload de anexos com validação; importação de livro por arquivo | `backend` `feature` |
| BE | OpenAPI 3 manual + Swagger UI + teste de contrato | `backend` `docs` |
| BE | LangSmith tracing opcional + endpoint de feedback | `observability` |
| BE | Busca semântica MVP (hash embeddings) | `ai` |
| FE | Chat UI completa (sessões, tema, thinking modes, anexos, áudio, markdown) | `frontend` |
| FE | Tela de biblioteca (CRUD + import + busca) | `frontend` |
| QA | 13 testes integração backend (82% cov), 4 Vitest, 5 e2e Playwright | `testing` |
| INFRA | Makefile, Docker Compose com healthchecks, coleção Postman | `infra` |

## Fluxo dos cards restantes por sprint (ver `03_ROADMAP.md`)

- Sprint 1 → MS-001, MS-003, MS-004, MS-101, MS-102 (18 pts)
- Sprint 2 → MS-002, MS-006, MS-103, MS-603 (21 pts)
- Sprint 3 → MS-201, MS-202, MS-501 (18 pts)
- Sprint 4 → MS-301, MS-401, MS-502, MS-503 (23 pts)
- Sprint 5 → MS-601, MS-602, MS-005, MS-104, MS-203, MS-302, MS-402, MS-403 (34 pts — refinar/dividir)
