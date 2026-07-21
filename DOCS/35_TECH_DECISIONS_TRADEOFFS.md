# Decisoes tecnicas e tradeoffs

## Backend

| Escolha | Por que faz sentido | Vantagens | Tradeoffs / riscos | Alternativas |
| --- | --- | --- | --- | --- |
| Python 3.12+ | Ecossistema forte para IA, APIs e testes. | Produtivo, legivel, bom suporte a LangChain/SQLAlchemy. | Performance depende de desenho de IO e workers. | Node, Go, Java/Kotlin. |
| Flask 3 | API pequena, prova backend e controle explicito. | Simples, flexivel, baixo overhead. | Menos opinativo que FastAPI; schemas e docs exigem disciplina. | FastAPI, Django REST. |
| Flask-SQLAlchemy/SQLAlchemy | ORM maduro e conhecido. | Modelagem relacional, queries expressivas, facil teste. | Precisa migracoes versionadas para producao. | SQLModel, Django ORM, Prisma. |
| SQLite | Setup local simples e zero infra. | Excelente para MVP, testes e demos. | Concorrencia limitada, backup/operacao simples demais para escala. | Postgres, MySQL. |
| `db.create_all()` | Acelera primeiro run local. | Menos passos para avaliador/dev. | Nao versiona schema e pode mascarar migracoes quebradas. | Alembic/Flask-Migrate. |
| Gateway local deterministico | Rodar sem chaves e sem custo. | Testes estaveis, onboarding rapido. | Nao mede qualidade real do LLM. | Mocks por teste, fixtures gravadas. |
| LangChain OpenAI-compatible | Reutiliza interface para OpenAI e HF router. | Troca de provedor mais simples. | Dependencia extra e diferencas sutis de parametros por modelo. | SDK OpenAI direto, LiteLLM. |
| LangSmith opcional | Observabilidade de chains e feedback. | Bom para depurar prompts e runs. | Custo/privacidade e dependencia externa. | OpenTelemetry, logs proprios. |
| pypdf | Extracao local de texto PDF. | Sem servico externo, suficiente para PDFs textuais. | PDFs escaneados nao funcionam; pode ser pesado. | OCR, unstructured.io, PyMuPDF. |

## Frontend

| Escolha | Por que faz sentido | Vantagens | Tradeoffs / riscos | Alternativas |
| --- | --- | --- | --- | --- |
| React 19 | Padrao comum para UI rica. | Ecossistema amplo, componentes testaveis. | Exige disciplina de estado e separacao de responsabilidades. | Vue, Svelte, Solid. |
| Vite | Dev server e build modernos. | Rapido, simples, boa integracao com Vitest. | Dependencias nativas podem falhar em sandbox/Windows restritivo. | Next.js, CRA, Rsbuild. |
| TypeScript | Tipagem do contrato e UI. | Reduz erros de props/payloads. | Tipos manuais podem divergir do backend. | JS puro, geracao via OpenAPI. |
| TanStack Query | Estado servidor/cache. | Invalida queries, retries e async state de forma limpa. | Precisa chaves consistentes e invalidacao correta. | SWR, RTK Query. |
| Tailwind CSS 4 | Design tokens e composicao rapida. | Produtividade e padrao visual consistente. | CSS pode ficar acoplado ao markup; classes longas. | CSS Modules, Panda, vanilla-extract. |
| Framer Motion | Animacoes e gestos. | Boa UX para sidebar/swipe. | Acessibilidade precisa ser implementada separadamente. | CSS transitions, Radix gestures. |
| react-markdown + remark-gfm | Renderizacao segura de Markdown. | Evita HTML perigoso por default e suporta GFM. | Highlight e copy code precisam componentes customizados. | MDX, markdown-it. |
| Playwright | Teste e2e real. | Excelente para fluxos de UI. | `channel: chrome` aumenta dependencia do ambiente. | Cypress, Vitest browser mode. |

## DevOps e qualidade

| Escolha | Por que faz sentido | Vantagens | Tradeoffs / riscos | Alternativas |
| --- | --- | --- | --- | --- |
| Docker Compose | Orquestracao local simples. | Um comando para backend/frontend. | Compose atual usa dev server Flask, nao WSGI de producao. | Kubernetes, Railway/Fly configs. |
| Makefile | Padroniza comandos. | Bom para Linux/macOS/CI. | Windows precisa adaptacao ou scripts PowerShell. | Taskfile, npm scripts raiz, Just. |
| Ruff | Lint Python rapido. | Baixo custo, bom default. | Config atual nao exige format no Makefile. | Black+Flake8, PyLint. |
| Pytest | Testes backend. | Fixtures simples, boa cobertura de casos. | Precisa controlar temp/cache no Windows sandbox. | unittest, nose2. |
| Vitest | Testes frontend integrados ao Vite. | Rapido e natural para TS/React. | Depende de config Vite carregar corretamente. | Jest, Web Test Runner. |

## Decisao: manter gateway local como default

Decisao recomendada: manter `CHAT_GATEWAY=local` no `.env.example`.

Motivos:

- Evita exigir chave externa no primeiro run.
- Mantem CI deterministicamente verde.
- Permite avaliar arquitetura sem custo.

Tradeoff:

- Demos locais nao refletem qualidade de um modelo real.

Mitigacao:

- Documentar claramente o modo ativo.
- Adicionar smoke tests opcionais para provedores reais em ambiente com secrets.

## Decisao: migrar para Postgres somente quando houver multiusuario

SQLite e suficiente para MVP e avaliacao tecnica. A migracao para Postgres deve acontecer junto com:

- Auth e ownership.
- Migracoes Alembic.
- Paginacao.
- Backup/restore formal.
- Observabilidade de queries.

Migrar antes disso aumenta complexidade sem resolver o maior risco atual: ausencia de controle de acesso.
