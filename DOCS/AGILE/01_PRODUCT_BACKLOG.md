# Product Backlog — MindSight AI

Cada item referencia o achado de auditoria (F-xx) em `04_AUDIT_FINDINGS.md` quando aplicável.
Formato: ID, história, critérios de aceite, labels, prioridade, estimativa (story points).

---

## Épico 1 — Fundação e Higiene do Repositório

### MS-001 — Versionar o projeto (primeiro commit)
> **Como** time, **quero** o repositório versionado com histórico limpo, **para** não perder trabalho e habilitar PRs/CI. (F-06)

- **Aceite:** commit inicial criado; `DOCS/` removido do `.gitignore` (F-16); remoto configurado; branch protegida.
- Labels: `infra`, `docs` · Prioridade: **P0** · Estimativa: **2**

### MS-002 — README raiz e limpeza de docs
> **Como** novo dev, **quero** um README na raiz com setup, arquitetura e comandos, **para** onboarding em < 15 min. (F-21, F-22)

- **Aceite:** README raiz cobre setup/test/run; `frontend/README.md` substituído; DOCS/33 corrigido (13 testes); DOCS/04 e 30 marcados como aspiracionais ou atualizados.
- Labels: `docs` · Prioridade: **P1** · Estimativa: **3**

### MS-003 — Corrigir lint e elevar gates de qualidade
> **Como** time, **quero** lint zero e gate de cobertura no Makefile, **para** que `make lint`/`make test` sejam confiáveis. (F-13, F-17)

- **Aceite:** Ruff sem erros (E501 em `openapi.py:83,327`); `backend-test-cov` usa `--cov-fail-under=80`; `make test` falha se cobertura < 80%.
- Labels: `testing`, `backend` · Prioridade: **P0** · Estimativa: **1**

### MS-004 — Sanear variáveis de ambiente e secrets
> **Como** dev, **quero** `.env.example` completo e sem secrets órfãs, **para** configurar qualquer ambiente sem ler código. (F-07, F-08)

- **Aceite:** `CHAT_GATEWAY` e `SECRET_KEY` documentados em `.env.example`; `HUGGINGFACE_API_KEY` removida do `.env` (ou implementada); prod exige `SECRET_KEY` não-default (falha no boot).
- Labels: `security`, `infra` · Prioridade: **P0** · Estimativa: **2**

### MS-005 — Remover dependências mortas
> **Como** time, **quero** dependências declaradas = dependências usadas, **para** reduzir superfície e confusão. (F-18, F-19)

- **Aceite:** `marshmallow` removido (ou adotado na validação); decisão registrada para `@tanstack/react-router`, `zod`, MSW (usar ou remover).
- Labels: `refactor` · Prioridade: **P2** · Estimativa: **2**

### MS-007 — Corrigir build do Docker Compose (pnpm v11 / esbuild)
> **Como** dev, **quero** `docker compose up --build` funcionando, **para** subir backend e frontend sem ajustes manuais. (F-31)

- **Aceite:** build do frontend não falha com `ERR_PNPM_IGNORED_BUILDS`; `pnpm-workspace.yaml` com `allowBuilds: {esbuild: true}` (pnpm v11 removeu `onlyBuiltDependencies`); Dockerfile copia `pnpm-workspace.yaml` antes do install; `docker compose up -d` deixa ambos os containers `healthy`.
- Labels: `bug`, `infra`, `frontend` · Prioridade: **P1** · Estimativa: **2**

### MS-006 — Pipeline CI com quality gates
> **Como** time, **quero** CI rodando lint + testes + cobertura + build a cada PR, **para** impedir regressões. (F-25, DOCS/25)

- **Aceite:** workflow GitHub Actions com jobs backend (ruff, pytest+cov≥80) e frontend (eslint, tsc, vitest, build); status obrigatório para merge.
- Labels: `infra`, `testing` · Prioridade: **P1** · Estimativa: **5**

---

## Épico 2 — IA Conversacional Real (LangChain)

### MS-101 — Histórico multi-turn no fluxo LangChain
> **Como** usuário, **quero** que o assistente lembre o contexto da conversa, **para** fazer perguntas de acompanhamento. (F-02)

- **Aceite (TDD):** teste red: pergunta de follow-up ("e quem o escreveu?") responde usando turno anterior; gateway recebe janela das últimas N mensagens da sessão; truncamento por tokens documentado; teste com gateway local + fake do LangChain.
- Labels: `ai`, `feature`, `backend` · Prioridade: **P0** · Estimativa: **5**

### MS-102 — Anexos como contexto da IA
> **Como** usuário, **quero** que arquivos enviados sejam considerados na resposta, **para** perguntar sobre meus documentos. (F-01)

- **Aceite (TDD):** texto de anexos `.txt/.md/.json/.pdf` extraído e injetado no prompt com limite de tamanho; resposta cita o anexo; teste de integração com upload + pergunta; anexo grande truncado com aviso.
- Labels: `ai`, `feature`, `backend` · Prioridade: **P0** · Estimativa: **8**

### MS-103 — Streaming SSE real do LLM
> **Como** usuário, **quero** ver a resposta sendo gerada token a token, **para** ter feedback imediato. (F-04)

- **Aceite (TDD):** `POST /chat/messages` passa a suportar modo stream (ou novo fluxo) que conecta `ChatOpenAI.stream()` ao SSE; gateway local também streama (para testes); mensagem persistida ao final; contrato OpenAPI atualizado.
- Labels: `ai`, `feature`, `backend` · Prioridade: **P1** · Estimativa: **8**

### MS-105 — Extração real de texto de PDF
> **Como** usuário, **quero** que uploads `.pdf` tenham o texto extraído de verdade, **para** importar livros e anexar PDFs ao chat com conteúdo legível. (F-29, Bugbot)

- **Aceite (TDD):** `pypdf` (ou similar) extrai texto de PDF no import e em `read_attachment_text`; PDF sem texto (escaneado) retorna aviso claro; teste com PDF fixture.
- Labels: `bug`, `backend` · Prioridade: **P2** · Estimativa: **3**

### MS-104 — Importação de livro com LLM de verdade
> **Como** usuário, **quero** que a "importação com IA" use o LLM quando disponível, **para** extrair metadados de textos não estruturados. (F-15)

- **Aceite:** quando `CHAT_GATEWAY=openai`, extração usa LangChain com saída estruturada; fallback heurístico mantido para `local`; UI deixa claro o modo ativo; testes para ambos os caminhos.
- Labels: `ai`, `feature` · Prioridade: **P2** · Estimativa: **5**

---

## Épico 3 — RAG e Busca Semântica

### MS-201 — Embeddings reais + FAISS
> **Como** usuário, **quero** busca semântica com embeddings reais, **para** encontrar livros por significado e não por hash. (F-03)

- **Aceite (TDD):** `SemanticSearchService` usa sentence-transformers (`EMBEDDING_MODEL`) + FAISS persistido em `FAISS_INDEX_PATH`; interface `EmbeddingModel` mantém o hash como fake de teste (Strategy); testes não baixam modelo no CI.
- Labels: `ai`, `feature`, `backend` · Prioridade: **P1** · Estimativa: **8**

### MS-202 — Indexar livros cadastrados no vector store
> **Como** usuário, **quero** que os livros que cadastro sejam pesquisáveis semanticamente, **para** o chat citar minha biblioteca via RAG. (F-03)

- **Aceite:** criar/importar livro indexa título+resumo; `ChatService` consulta o índice (substituindo/complementando o scoring lexical); reindexação via comando (`make reindex` ou endpoint admin); testes de integração.
- Labels: `ai`, `feature`, `backend` · Prioridade: **P1** · Estimativa: **5**

### MS-203 — UI de busca semântica
> **Como** usuário, **quero** buscar semanticamente pela interface, **para** usar o recurso sem Postman. (F-20)

- **Aceite:** tela/aba na biblioteca consumindo `POST /semantic-search` (client já existe); estados de loading/erro/vazio; testes Vitest + e2e.
- Labels: `frontend`, `feature` · Prioridade: **P2** · Estimativa: **3**

---

## Épico 4 — Segurança

### MS-301 — Autenticação por API key/token
> **Como** operador, **quero** endpoints protegidos, **para** impedir uso anônimo da API e gasto de tokens do LLM. (F-05)

- **Aceite (TDD):** middleware/decorator de auth (API key via header como mínimo); `/health`, `/docs`, `/openapi.json` públicos; 401 padronizado no formato de erro; frontend envia credencial; testes 401/403/200.
- Labels: `security`, `backend`, `frontend` · Prioridade: **P1** · Estimativa: **8**

### MS-302 — Hardening de produção
> **Como** operador, **quero** configuração de produção segura, **para** deploy sem riscos óbvios. (F-05, F-09)

- **Aceite:** `ProductionConfig` falha sem `SECRET_KEY` forte; CORS configurável por env em prod; Dockerfile com opção de instalar `requirements-ai.txt` (build arg); rate limiting básico no chat.
- Labels: `security`, `infra` · Prioridade: **P2** · Estimativa: **5**

---

## Épico 5 — Observabilidade e Métricas

### MS-401 — Logs estruturados + request ID
> **Como** operador, **quero** logs JSON com request_id gerado por requisição, **para** rastrear falhas. (F-10)

- **Aceite:** middleware gera `request_id` (uuid) quando ausente e propaga ao response e logs; `LOG_LEVEL` respeitado; logs JSON com rota, status, latência; testes do middleware.
- Labels: `observability`, `backend` · Prioridade: **P1** · Estimativa: **5**

### MS-402 — Métricas Prometheus
> **Como** operador, **quero** `/metrics` com latência, contadores por endpoint e tokens LLM, **para** monitorar a API. (F-10, DOCS/24)

- **Aceite:** endpoint `/metrics`; histograma de latência por rota; contador de erros; contador de chamadas/tokens do gateway IA; teste de presença das métricas.
- Labels: `observability`, `backend` · Prioridade: **P2** · Estimativa: **5**

### MS-403 — Feedback LangSmith na UI
> **Como** usuário, **quero** avaliar respostas (👍/👎), **para** alimentar a melhoria do assistente. (F-20)

- **Aceite:** botões de feedback no `MessageBubble` chamando `POST /chat/messages/{id}/feedback`; estado otimista; quando LangSmith desligado, UI esconde ou mostra aviso discreto; testes.
- Labels: `frontend`, `observability` · Prioridade: **P2** · Estimativa: **3**

---

## Épico 6 — Qualidade e Pirâmide de Testes

### MS-501 — Base da pirâmide: testes unitários puros no backend
> **Como** dev, **quero** testes unitários de services/repositories sem HTTP, **para** ter pirâmide correta (muitos unitários, médios de integração, poucos e2e). (F-11)

- **Aceite:** unitários para `parse_book_payload`, scoring, `BookMetadataExtractor`, `normalize_thinking_mode`, gateways (com fakes); execução < 1s; integração HTTP mantida; meta ≥ 60% dos testes unitários.
- Labels: `testing`, `backend` · Prioridade: **P1** · Estimativa: **5**

### MS-502 — E2E full stack real
> **Como** time, **quero** ao menos um fluxo e2e com backend real (sem mock), **para** validar o sistema integrado. (F-12)

- **Aceite:** job/perfil Playwright sobe backend (gateway `local`) + frontend e percorre: criar livro → perguntar ao chat → resposta cita o livro; roda no CI; mantém suíte mockada para velocidade.
- Labels: `testing`, `infra` · Prioridade: **P1** · Estimativa: **5**

### MS-503 — Testes frontend dos fluxos críticos
> **Como** dev, **quero** testes de envio de mensagem, upload e import de livro, **para** proteger os fluxos principais. (F-12, F-20)

- **Aceite:** Vitest/RTL cobrindo: enviar mensagem (happy + erro), anexar arquivo, importar livro; MSW adotado ou fetch stub padronizado; cobertura frontend reportada no CI.
- Labels: `testing`, `frontend` · Prioridade: **P1** · Estimativa: **5**

---

## Épico 7 — Refatoração e Clean Architecture

### MS-601 — Quebrar `App.tsx` em features
> **Como** dev, **quero** `App.tsx` (~1130 linhas) dividido por feature, **para** respeitar SRP e facilitar testes. (F-14)

- **Aceite:** extrair `features/chat/` (Sidebar, Header, MessageList, Composer) e `features/library/` (BooksAdminView, BookCard); `App.tsx` < 200 linhas; nenhum teste quebra; sem mudança visual.
- Labels: `refactor`, `frontend` · Prioridade: **P1** · Estimativa: **8**

### MS-602 — Consertar vazamentos de camada no backend
> **Como** dev, **quero** rotas falando só com services, **para** manter a Clean Architecture consistente. (F-23, F-24)

- **Aceite:** `chat.py` e `attachments.py` deixam de acessar repositório/model direto; scoring lexical movido de `repositories.py` para service/domínio; testes existentes verdes.
- Labels: `refactor`, `backend` · Prioridade: **P2** · Estimativa: **3**

### MS-604 — Corrigir retry que duplica sessões no frontend
> **Como** usuário, **quero** que reenviar uma mensagem que falhou não crie outra conversa, **para** não poluir meu histórico. (F-30, Bugbot)

- **Aceite (TDD):** `selectedSessionId` atualizado assim que a sessão é criada (não só em `onSuccess`); retry reusa a mesma sessão; teste Vitest do fluxo de falha + retry.
- Labels: `bug`, `frontend` · Prioridade: **P1** · Estimativa: **2**

### MS-603 — SSE/streaming consumido no frontend
> **Como** usuário, **quero** ver a resposta aparecer progressivamente na UI, **para** uma experiência de chat moderna. (F-04, F-20; depende de MS-103)

- **Aceite:** UI consome SSE com render incremental e fallback para resposta completa; indicador de "digitando"; testes do hook de streaming.
- Labels: `frontend`, `feature` · Prioridade: **P1** · Estimativa: **5**

---

## Resumo

| Épico | Itens | Pontos |
|---|---|---|
| 1 — Fundação | MS-001..006 | 15 |
| 2 — IA Conversacional | MS-101..104 | 26 |
| 3 — RAG | MS-201..203 | 16 |
| 4 — Segurança | MS-301..302 | 13 |
| 5 — Observabilidade | MS-401..403 | 13 |
| 6 — Testes | MS-501..503 | 15 |
| 7 — Refatoração | MS-601..603 | 16 |
| **Total** | **21 itens** | **114 pts** |
