# Roadmap — MindSight AI

Sprints de 1 semana. Capacidade assumida: ~18–22 pts/sprint (ajustar após Sprint 1 com velocity real).

## Milestone M1 — Fundação Sólida (Sprint 1)

**Objetivo:** repositório versionado, gates de qualidade confiáveis e o núcleo de IA conversacional correto.

| Item | Título | Pts |
|---|---|---|
| MS-001 | Primeiro commit + DOCS versionados | 2 |
| MS-003 | Lint zero + gate de cobertura | 1 |
| MS-004 | Sanear .env e secrets | 2 |
| MS-101 | Histórico multi-turn no LLM | 5 |
| MS-102 | Anexos como contexto da IA | 8 |

**Critério do milestone:** conversa multi-turn funcional com anexos; `make lint`/`make test` estritos; repo no git.

## Milestone M2 — Experiência de Chat Completa (Sprint 2)

**Objetivo:** streaming real de ponta a ponta e CI protegendo tudo.

| Item | Título | Pts |
|---|---|---|
| MS-103 | Streaming SSE real do LLM | 8 |
| MS-603 | Streaming consumido na UI | 5 |
| MS-006 | Pipeline CI com quality gates | 5 |
| MS-002 | README raiz + sync de docs | 3 |

**Critério:** resposta aparece token a token na UI; CI verde obrigatório para merge.

## Milestone M3 — RAG de Verdade (Sprint 3)

**Objetivo:** substituir o MVP de hash por embeddings reais e indexar a biblioteca.

| Item | Título | Pts |
|---|---|---|
| MS-201 | Embeddings reais + FAISS | 8 |
| MS-202 | Indexar livros no vector store | 5 |
| MS-501 | Testes unitários puros (base da pirâmide) | 5 |

**Critério:** chat responde com RAG sobre livros cadastrados; pirâmide de testes correta.

## Milestone M4 — Pronto para Produção (Sprint 4)

**Objetivo:** segurança, observabilidade e validação full stack.

| Item | Título | Pts |
|---|---|---|
| MS-301 | Autenticação por API key | 8 |
| MS-401 | Logs estruturados + request ID | 5 |
| MS-502 | E2E full stack real | 5 |
| MS-503 | Testes frontend dos fluxos críticos | 5 |

**Critério:** API protegida, rastreável e validada de ponta a ponta no CI.

## Milestone M5 — Polimento e Dívidas (Sprint 5+)

**Objetivo:** refatorações estruturais e features secundárias. Dividir em 2 sprints se a velocity confirmar ~20 pts.

| Item | Título | Pts |
|---|---|---|
| MS-601 | Quebrar App.tsx em features | 8 |
| MS-602 | Vazamentos de camada backend | 3 |
| MS-005 | Dependências mortas | 2 |
| MS-104 | Import de livro com LLM real | 5 |
| MS-203 | UI de busca semântica | 3 |
| MS-302 | Hardening de produção | 5 |
| MS-402 | Métricas Prometheus | 5 |
| MS-403 | Feedback LangSmith na UI | 3 |

## Visão de linha do tempo

```
Sprint 1   Sprint 2   Sprint 3   Sprint 4   Sprint 5   Sprint 6
   M1   →    M2    →    M3    →    M4    →       M5 (split)
Fundação  Streaming    RAG       Prod-      Refactor + extras
+ IA core + CI         real      ready
```

## Riscos e dependências

| Risco | Mitigação |
|---|---|
| MS-201 baixa modelo no CI (lento/flaky) | Interface `EmbeddingModel` com fake de hash nos testes; cache de modelo no CI |
| MS-103/MS-603 acoplados | Definir contrato SSE antes (evento `token`, `done`, `error`) e desenvolver em paralelo com gateway local |
| MS-301 quebra frontend/Postman | Feature flag `AUTH_ENABLED` durante a transição; atualizar `collection.json` |
| Custo de tokens OpenAI em testes | Sempre usar `CHAT_GATEWAY=local` em CI; testes com LangChain via fakes |
