# Status de implementacao

Auditoria realizada em 2026-07-03.

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
| Persistencia | MVP | SQLite + SQLAlchemy; sem migracoes versionadas. |
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

1. Preparar WSGI para producao.
2. Adicionar autenticacao/autorizacao e ownership.
3. Substituir migracoes ad hoc por Alembic/Flask-Migrate.
4. Manter OpenAPI, backend e tipos frontend alinhados por testes de contrato.
5. Tornar uploads transacionais e adicionar limpeza de anexos orfaos.
6. Adicionar paginacao, rate limit e timeouts.
7. Refatorar frontend por dominios e incluir mais logica no coverage.
