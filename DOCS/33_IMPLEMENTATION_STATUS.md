# Status de implementacao

Auditoria realizada em 2026-07-03. Atualizado em 2026-07-21 apos o fechamento das Fases 0-3 (hardening de backend, migrations reais, autenticacao minima e WSGI de producao).

## Backend

| Area | Status | Observacoes |
| --- | --- | --- |
| App factory Flask | Implementado | `create_app` registra blueprints, CORS e handlers. |
| Health check | Implementado | `/health` e `/api/v1/health`. |
| Livros | Implementado | Criacao, listagem, busca e detalhe. |
| Importacao de livros | Implementado | TXT/MD/JSON/PDF com extracao heuristica. |
| Chat | Implementado | Sessoes, mensagens, historico, contexto de livros e anexos. |
| SSE | Parcial | Emite playback da mensagem persistida, nao stream real do LLM. |
| Gateways IA | Parcial | Local, OpenAI-compatible, HF router; timeout e rate limit por IP em produção; sem retry com backoff. |
| LangSmith | Parcial | Tracing/feedback opcional com no-op resiliente. |
| Uploads | Parcial | Valida extensao/tamanho e remove arquivos ao deletar sessao; ainda precisa hardening e transacao de envio. |
| Busca semantica | Demo | Hashing local; config de FAISS/embeddings ainda nao efetivada. |
| Persistencia | Implementado | SQLite + SQLAlchemy com migracoes versionadas (Alembic/Flask-Migrate). |
| Autenticacao | Implementado (minima) | Segredo compartilhado via `API_KEY`/`Authorization: Bearer`; sem contas de usuario nem ownership (fora do escopo do MVP, ver visao de produto). Boot em producao falha sem segredos reais. |
| WSGI de producao | Implementado | Container roda Gunicorn (`--preload` + `post_fork` para migration/engine seguros com multiplos workers), nao mais o dev server do Flask. |
| OpenAPI | Parcial | Documento manual; enum de status do chat alinhado a `failed`. |

## Frontend

| Area | Status | Observacoes |
| --- | --- | --- |
| Shell de chat | Implementado | Layout responsivo com sidebar e composer. |
| Biblioteca | Implementado | Cadastro, filtros, importacao e acao "perguntar a IA". |
| API client | Implementado | Cliente HTTP isolado e testado. |
| Markdown | Implementado | `react-markdown` com GFM, highlight e botao copiar. |
| Anexos | Implementado | Validacao local, preview de imagem e upload. |
| Audio | Parcial | Grava via MediaRecorder; sem transcricao real dedicada. |
| Tema | Implementado | Claro/escuro persistido em localStorage. |
| E2E | Parcial | Playwright cobre shell e biblioteca, mas depende de Chrome. |
| Acessibilidade | Implementado | Drawer mobile com `role=dialog`, `aria-modal`, focus trap e Escape; pin/delete de sessão já tinha alternativa por teclado desde a Fase 1. |
| Modularidade | Parcial | `App.tsx` concentra muitas responsabilidades (fora do escopo do gate de cobertura, mas coberto por testes de integração em `App.test.tsx`). |
| Busca de conversas | Implementado | Filtro por título na sidebar. |

## Testes e verificacoes

Resultado local da auditoria:

| Comando | Resultado |
| --- | --- |
| `backend/.venv/Scripts/python.exe -m ruff check app tests` | Passou. |
| `backend/.venv/Scripts/python.exe -m compileall app` | Passou. |
| `frontend pnpm typecheck` | Passou. |
| `frontend pnpm lint` | Passou. |
| `frontend pnpm test` | Passou: 9 arquivos, 64 testes. |
| `backend pytest` | Tentado; bloqueado por permissao no diretorio temporario do sandbox. |

## Pendencias mais relevantes

1. Streaming real do provedor (hoje a rota SSE reproduz uma mensagem ja persistida).
2. Refatorar `App.tsx` (1611 linhas) por dominios — `features/chat`, `features/books`, `features/settings`.
3. Conectar a busca semantica aos livros reais (hoje indexa 6 documentos fixos).
4. Metricas de operacao (latencia, erros, chamadas LLM).
5. Retry com backoff no gateway de IA (timeout ja existe; falha ainda nao tenta novamente).
6. Limpeza de anexos orfaos definitivos (o cleanup client-side existe; falta um job de backstop para o caso de o proprio cleanup falhar).

Concluidas desde a auditoria original: WSGI de producao, autenticacao minima por API key, guarda de config insegura em producao, migracoes Alembic, paginacao, compensacao de anexos orfaos apos falha no envio da mensagem, timeout do gateway de IA, rate limiting no endpoint de chat, `request_id` gerado/correlacionado, `LOG_LEVEL` aplicado globalmente, acessibilidade do drawer mobile, busca de conversas por titulo, cleanup do microfone no unmount, e remocao de dependencias mortas (`@tanstack/react-router`, `zod`).
