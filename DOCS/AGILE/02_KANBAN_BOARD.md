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
| MS-001 | Primeiro commit + DOCS fora do .gitignore | `infra` `docs` | **P0** | 2 |
| MS-003 | Lint zero + gate cobertura no Makefile | `testing` `backend` | **P0** | 1 |
| MS-004 | Sanear .env (CHAT_GATEWAY, SECRET_KEY, HF key órfã) | `security` `infra` | **P0** | 2 |
| MS-101 | Histórico multi-turn no LangChain | `ai` `feature` `backend` | **P0** | 5 |
| MS-102 | Anexos como contexto da IA | `ai` `feature` `backend` | **P0** | 8 |

### 🔨 In Progress

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| — | *(vazio — aguardando início da Sprint 1)* | | | |

### 🔍 Review/QA

| Card | Título | Labels | Prioridade | Pts |
|---|---|---|---|---|
| — | *(vazio)* | | | |

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
