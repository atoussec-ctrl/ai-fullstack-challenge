# Backlog Fullstack

## Épico A — Setup

| ID | Task | Prioridade | Critério |
|---|---|---:|---|
| SETUP-001 | Criar monorepo | Alta | Estrutura documentada existe |
| SETUP-002 | Configurar backend Flask | Alta | `/health` responde |
| SETUP-003 | Configurar frontend Vite TS | Alta | `pnpm dev` roda |
| SETUP-004 | Configurar Tailwind e shadcn/ui | Alta | Button renderiza |
| SETUP-005 | Configurar CI | Média | Pipeline roda |

## Épico B — Backend prova

| ID | Task | Prioridade | Critério |
|---|---|---:|---|
| BE-001 | Entidade Book | Alta | Teste unitário |
| BE-002 | POST /books | Alta | Teste endpoint |
| BE-003 | GET /books | Alta | Busca por título/autor |
| BE-004 | SQLite repository | Alta | Teste integração |
| BE-005 | OpenAPI Flask | Alta | `/openapi.json` disponível |
| BE-006 | FastAPI parity | Média | Contratos equivalentes |

## Épico C — IA

| ID | Task | Prioridade | Critério |
|---|---|---:|---|
| AI-001 | Prompt Python assistant | Alta | Teste de prompt |
| AI-002 | LangChain gateway | Alta | Fake em teste |
| AI-003 | Endpoint chat | Alta | Retorna processing |
| AI-004 | Streaming | Média | SSE funciona |
| AI-005 | LangSmith tracing | Média | Env habilita |
| AI-006 | Semantic search FAISS | Alta | Top-k retorna resultado |

## Épico D — Frontend chat

| ID | Task | Prioridade | Critério |
|---|---|---:|---|
| FE-001 | AppShell | Alta | Desktop e mobile |
| FE-002 | ChatSidebar | Alta | Lista sessões |
| FE-003 | MessageList | Alta | Render mensagens |
| FE-004 | ChatComposer | Alta | Envia com Enter |
| FE-005 | Thinking selector | Alta | Payload correto |
| FE-006 | Theme toggle | Alta | Persiste tema |
| FE-007 | Attachment tray | Alta | Preview e remove |
| FE-008 | Audio recorder | Média | Grava e anexa |
| FE-009 | Streaming UI | Média | Tokens aparecem |
| FE-010 | Empty state | Média | Sugestões Python |

## Épico E — Testes

| ID | Task | Prioridade | Critério |
|---|---|---:|---|
| QA-001 | Vitest setup | Alta | Teste exemplo |
| QA-002 | RTL setup | Alta | Componente testado |
| QA-003 | MSW setup | Alta | API mockada |
| QA-004 | Playwright setup | Alta | E2E smoke |
| QA-005 | Storybook setup | Média | Stories principais |
| QA-006 | Coverage | Média | Relatório gerado |
