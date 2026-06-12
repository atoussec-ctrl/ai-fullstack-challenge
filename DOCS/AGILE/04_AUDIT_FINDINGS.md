# Audit Findings — MindSight AI

Data: 2026-06-11
Escopo: código, testes, infra, endpoints, configuração, API keys, observabilidade, design patterns.

## Verificação executada (evidências)

| Verificação | Resultado |
|---|---|
| Backend pytest (13 testes) | ✅ 13 passed, cobertura **81.85%** (gate 80% do `pyproject.toml` atingido) |
| Frontend Vitest (4 testes) | ✅ 4 passed |
| Playwright e2e (6 cenários) | ✅ 5 passed, 1 skipped (cenário mobile-only em desktop) |
| `tsc --noEmit` | ✅ sem erros |
| ESLint | ✅ sem erros |
| Ruff backend | ❌ **2 erros E501** (linhas longas) em `app/routes/openapi.py:83` e `:327` |
| Smoke test live de todos os endpoints | ✅ health, books (criar/validar/buscar/404), chat (sessão/mensagem/SSE/feedback), semantic-search, attachments (rejeição `.exe`), openapi (12 paths) |
| Git | ⚠️ repositório **sem nenhum commit** e sem remoto — `/babysit` (PR) não aplicável |

## Achados por severidade

### Severidade ALTA

| ID | Achado | Evidência |
|---|---|---|
| F-01 | **Anexos não entram no contexto da IA** — upload funciona e vincula à mensagem, mas o conteúdo nunca é lido pelo gateway LLM | `backend/app/services/chat.py` (`ChatService.ask`) |
| F-02 | **Sem histórico multi-turn** — cada pergunta vai isolada ao LLM; o fluxo de conversação não usa as mensagens anteriores da sessão | `chat.py`: gateway recebe só `question` + contexto de livros |
| F-03 | **RAG/FAISS não implementado** — `.env` configura FAISS e sentence-transformers, mas `SemanticSearchService` usa 6 documentos hardcoded e embedding por hash determinístico; livros cadastrados não são indexados | `backend/app/services/semantic_search.py` |
| F-04 | **Streaming SSE é fake** — `GET /chat/messages/{id}/stream` apenas re-fatia a resposta já persistida; frontend nem consome o endpoint | `backend/app/routes/chat.py` |
| F-05 | **Sem autenticação** em nenhum endpoint; `SECRET_KEY` default `"dev-secret-key-change-me"` | `backend/app/config.py` |
| F-06 | **Repositório sem commits** — todo o trabalho está unversionado; risco de perda total | `git log` vazio |

### Severidade MÉDIA

| ID | Achado | Evidência |
|---|---|---|
| F-07 | `HUGGINGFACE_API_KEY` real presente no `.env` mas **não usada em lugar nenhum do código** (secret órfã; `.env` está no `.gitignore`, ok, mas deve ser removida ou usada) | `.env` vs grep no código |
| F-08 | `CHAT_GATEWAY` e `SECRET_KEY` ausentes do `.env.example` — impossível ativar OpenAI sem ler código | `.env.example` |
| F-09 | Dockerfile do backend não instala `requirements-ai.txt` → LangChain/OpenAI indisponíveis no container | `backend/Dockerfile`, `docker-compose.yml` |
| F-10 | Observabilidade documentada mas não implementada: sem logs estruturados, sem métricas, `LOG_LEVEL` sem efeito, request ID só ecoado se enviado | `DOCS/24` vs código |
| F-11 | Pirâmide de testes invertida no backend: os 13 testes são de integração HTTP; **não há testes unitários puros** de services/repositories | `backend/tests/` |
| F-12 | E2E Playwright roda com **API 100% mockada** — nenhum teste valida frontend + backend reais juntos | `frontend/e2e/chat.spec.ts` |
| F-13 | Gate de cobertura existe no `pyproject.toml` mas o Makefile não falha por cobertura (sem `--cov-fail-under`) | `Makefile` vs `pyproject.toml` |
| F-14 | `App.tsx` monolítico (~1130 linhas) — viola SRP; doc 34 já recomendava split | `frontend/src/App.tsx` |
| F-15 | "Importar livro com IA" usa heurística/regex, não LLM — UI promete IA | `backend/app/services/book_import.py` |
| F-16 | `DOCS/` está no `.gitignore` — 35 documentos + estes ficariam fora do versionamento | `.gitignore` |
| F-17 | 2 erros de lint Ruff (E501) | `app/routes/openapi.py:83,327` |

### Severidade BAIXA

| ID | Achado | Evidência |
|---|---|---|
| F-18 | `marshmallow` declarado em `requirements.txt` e nunca usado | grep |
| F-19 | Dependências frontend instaladas e não usadas: `@tanstack/react-router`, `zod`; MSW documentado e ausente | `package.json` vs `src/` |
| F-20 | Frontend não consome: feedback LangSmith, semantic-search, SSE | `shared/api/client.ts` vs `App.tsx` |
| F-21 | Divergências docs vs código: estrutura `apps/` (DOCS/04, 30), FastAPI parity (DOCS/07) inexistente, DOCS/33 diz 11 testes (são 13) | `DOCS/` |
| F-22 | Sem README na raiz; `frontend/README.md` é template Vite genérico | raiz, `frontend/` |
| F-23 | Rotas acessando repositório/model direto em alguns pontos (`chat.py` lista sessões, `attachments.py` usa `Attachment.query`) — vaza camada | `routes/` |
| F-24 | Repository mistura persistência e scoring lexical (`score_book`) — responsabilidade de domínio/serviço | `repositories.py` |
| F-25 | Sem CI/CD — pipeline descrito em DOCS/25 não existe | `.github/` ausente |

## Achados adicionais do Bugbot (2026-06-11)

| ID | Achado | Severidade | Status |
|---|---|---|---|
| F-26 | Anexos de outra sessão podiam ser vinculados a qualquer mensagem (`attach_to_message` sem checagem de sessão) | Alta | ✅ Corrigido na Sprint 1 (validação em `ChatService._validated_attachments`) |
| F-27 | Falha do LLM deixava mensagem do usuário órfã e estourava exceção sem rollback | Média | ✅ Corrigido na Sprint 1 (mensagem assistant `status="failed"` com texto amigável) |
| F-28 | `reasoning_effort` enviado para modelos não-reasoning (ex.: `gpt-4.1-mini`) | Média | ✅ Corrigido na Sprint 1 (`chat_model_kwargs` por família de modelo) |
| F-29 | Import de livro `.pdf` decodifica bytes binários como UTF-8 (sem extração real de PDF) | Média | ✅ Corrigido (MS-105: `extract_pdf_text` com pypdf no import e em anexos) |
| F-30 | Retry de envio sem sessão selecionada cria sessões duplicadas no frontend (`createSession` dentro da mutation) | Média | ✅ Corrigido (MS-604: `setSelectedSessionId` logo após criar a sessão) |
| F-31 | `docker compose up --build` falha no frontend: pnpm v11 retorna `ERR_PNPM_IGNORED_BUILDS` (esbuild) e o Dockerfile não copiava o `pnpm-workspace.yaml` | Alta | ✅ Corrigido (MS-007: `allowBuilds: {esbuild: true}` no workspace + COPY no Dockerfile; validado `docker compose up` com containers healthy) |
| F-32 | Sem migrations versionadas: schema criado via `db.create_all()` + `_ensure_sqlite_schema()` (ALTER TABLE ad-hoc). Mudanças de schema mais complexas (renomear/remover coluna, constraints) ficam arriscadas | Média | 📋 Backlog → MS-008 (mitigado por seed idempotente + backup/restore — MS-009) |

## Pontos fortes confirmados

- Arquitetura em camadas limpa: routes → services → repositories → models (Clean Architecture pragmática).
- Padrões bem aplicados: Application Factory, Blueprint, Repository, **Strategy** (gateways de chat), DI leve para testes, decorator condicional para LangSmith.
- Erros padronizados (`{error: {code, message, details}, request_id}`) e validação consistente com mensagens claras.
- OpenAPI 3.0.3 manual + Swagger UI em `/docs`, com teste de contrato.
- LangSmith integrado de forma segura (no-op quando desligado) com `trace_id` persistido e endpoint de feedback.
- Gateway local determinístico permite testes herméticos sem API key (ótimo para TDD/CI).
- Upload com validação de extensão/tamanho dos dois lados, `.env` fora do git.
