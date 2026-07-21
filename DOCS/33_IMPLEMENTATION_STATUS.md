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
| Gateways IA | Parcial | Local, OpenAI-compatible, HF router; sem timeout/rate limit robusto. |
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
| Acessibilidade | Parcial | Falta modal semantics/focus trap no drawer e alternativa clara ao swipe. |
| Modularidade | Parcial | `App.tsx` concentra muitas responsabilidades. |

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

1. Adicionar timeout/retry e rate limit no gateway de IA.
2. Streaming real do provedor (hoje a rota SSE reproduz uma mensagem ja persistida).
3. Refatorar `App.tsx` (1611 linhas, fora do escopo do gate de cobertura) por dominios.
4. Conectar a busca semantica aos livros reais (hoje indexa 6 documentos fixos).
5. Acessibilidade do drawer mobile (`role=dialog`, `aria-modal`, focus trap, Escape).
6. Gerar `request_id` quando ausente e estruturar logs para correlacao.

Concluidas desde a auditoria original: WSGI de producao, autenticacao minima por API key, guarda de config insegura em producao, migracoes Alembic, paginacao, compensacao de anexos orfaos apos falha no envio da mensagem.
