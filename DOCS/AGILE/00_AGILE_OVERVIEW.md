# Agile Overview — MindSight AI

Data: 2026-06-11
Fonte: auditoria completa do código + testes executados (ver `04_AUDIT_FINDINGS.md`).

## Metodologia

Híbrido **Scrum + Kanban (Scrumban)**:

- **Scrum**: sprints de 1 semana, com Sprint Planning, Daily (assíncrona), Review e Retrospective.
- **Kanban**: fluxo contínuo no board (`02_KANBAN_BOARD.md`), WIP limit de 2 itens por pessoa em `In Progress`.
- **TDD obrigatório** em todo item de código: Red → Green → Refactor. PR sem teste novo não passa no gate.

## Papéis

| Papel | Responsabilidade |
|---|---|
| Product Owner | Prioriza o Product Backlog, valida critérios de aceite |
| Dev (fullstack) | Implementa com TDD, mantém pirâmide de testes |
| QA Gate | `make lint`, `make test`, cobertura ≥ 80%, e2e verde |

## Cerimônias

| Cerimônia | Cadência | Saída |
|---|---|---|
| Sprint Planning | Início da sprint | Sprint Backlog com itens "Ready" |
| Daily | Diária (assíncrona ok) | Bloqueios visíveis no board |
| Review | Fim da sprint | Demo dos incrementos |
| Retrospective | Fim da sprint | 1–3 ações de melhoria |
| Backlog Refinement | Meio da sprint | Itens com DoR completo |

## Definition of Ready (DoR)

- [ ] História com descrição no formato "Como/Quero/Para"
- [ ] Critérios de aceite testáveis listados
- [ ] Labels, prioridade e estimativa atribuídas
- [ ] Dependências identificadas

## Definition of Done (DoD)

- [ ] Ciclo TDD evidenciado (teste escrito antes, falhando, depois verde)
- [ ] Testes unitários + integração cobrindo o item; e2e quando toca fluxo de usuário
- [ ] `make lint` e `make typecheck` verdes
- [ ] Cobertura backend ≥ 80% (gate `--cov-fail-under=80`)
- [ ] OpenAPI (`/openapi.json`) e `collection.json` atualizados se o contrato mudou
- [ ] Documentação em `DOCS/` atualizada
- [ ] Sem secrets em código ou commits

## Labels

| Label | Uso |
|---|---|
| `bug` | Comportamento incorreto existente |
| `feature` | Funcionalidade nova |
| `refactor` | Melhoria estrutural sem mudar comportamento |
| `security` | Autenticação, secrets, hardening |
| `testing` | Pirâmide de testes, cobertura, e2e |
| `observability` | Logs, métricas, tracing, LangSmith |
| `ai` | LangChain, LLM, RAG, embeddings |
| `infra` | Docker, CI/CD, Makefile, env |
| `docs` | Documentação |
| `backend` / `frontend` | Área afetada |

## Prioridades

| Prioridade | Significado | SLA sugerido |
|---|---|---|
| `P0` | Bloqueia entrega/segurança | Sprint atual |
| `P1` | Alto valor / dívida crítica | Próxima sprint |
| `P2` | Importante, não urgente | Roadmap |
| `P3` | Desejável | Backlog frio |

## Estimativas

Story points (Fibonacci): 1, 2, 3, 5, 8, 13. Itens > 8 devem ser quebrados.

## Documentos

- `01_PRODUCT_BACKLOG.md` — backlog completo com épicos, histórias e critérios
- `02_KANBAN_BOARD.md` — board com colunas e cards
- `03_ROADMAP.md` — milestones e sprints
- `04_AUDIT_FINDINGS.md` — achados da auditoria que originaram o backlog
