# Decisões de Stack

## Frontend

| Categoria | Escolha | Motivo |
|---|---|---|
| Framework UI | React | Ecossistema forte e compatível com shadcn/ui |
| Build tool | Vite | Rápido, simples e bom suporte a TypeScript |
| Linguagem | TypeScript | Contratos mais seguros e melhor DX |
| UI base | shadcn/ui | Componentes acessíveis, customizáveis e compatíveis com Tailwind |
| Estilo | Tailwind CSS | Design tokens rápidos, tema claro/escuro e produtividade |
| Animações | Motion / Framer Motion | Transições suaves para chat, sidebar, menus e upload tray |
| Server state | TanStack Query | Cache, mutations, retries e invalidação |
| Router | TanStack Router | Rotas type-safe e bom suporte a URL state |
| Forms | TanStack Form + Zod | Formulários tipados e validação |
| Unit/component tests | Vitest + React Testing Library | Testes rápidos e próximos do usuário |
| API mocks | MSW | Mock HTTP realista para testes e Storybook |
| E2E | Playwright | Fluxos reais em browsers modernos |
| Component workshop | Storybook | Desenvolvimento isolado de componentes |
| Ícones | lucide-react | Compatível com shadcn/ui |

## Backend

| Categoria | Escolha | Motivo |
|---|---|---|
| Linguagem | Python 3.12+ | Exigência da prova e stack de IA |
| API principal | Flask | Alvo de integração do frontend |
| OpenAPI Flask | flask-smorest | Documentação Swagger/OpenAPI no Flask |
| API alternativa | FastAPI | Versão paralela moderna e nativa em OpenAPI |
| Banco | SQLite | Exigido pela prova |
| ORM | SQLAlchemy | Permite migração futura para PostgreSQL |
| LLM orchestration | LangChain | Fluxo de prompt e modelo |
| Observabilidade IA | LangSmith | Tracing e análise |
| Modelo | OpenAI configurável via env | Flexibilidade |
| Vector store MVP | FAISS | Local, simples e rápido |
| Vector store evolução | Milvus | Produção e escala |
| Testes | pytest | Padrão Python |
| Qualidade | Ruff + mypy | Lint, format e typecheck |

## Decisões complementares

### Por que React se o usuário citou Vite + TypeScript?

Vite é o build tool. Para usar shadcn/ui, Storybook React e componentes com arquitetura madura, a escolha natural é React com TypeScript.

### Por que TanStack Query e não apenas fetch?

Porque a aplicação terá histórico, conversas, mensagens, upload, streaming, retry e cache. TanStack Query reduz lógica manual e melhora consistência.

### Por que não colocar chamada OpenAI no frontend?

Porque a chave da OpenAI não deve ir para o browser. O frontend conversa com Flask, e Flask conversa com OpenAI.

### Por que manter FastAPI?

Porque a solicitação inicial mencionava versão Flask e FastAPI. Porém, o frontend será integrado ao Flask por decisão explícita do usuário.

### Por que FAISS no MVP?

FAISS reduz dependências operacionais. Milvus fica documentado como evolução para produção.
