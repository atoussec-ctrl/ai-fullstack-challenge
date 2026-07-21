# MindSight AI - Documentacao tecnica

Este pacote documenta a codebase fullstack atual, as escolhas tecnicas, os fluxos principais, os gaps encontrados e um roadmap pragmatico de melhoria.

## Leitura recomendada

| Documento | Quando usar |
| --- | --- |
| [01_PRODUCT_VISION.md](01_PRODUCT_VISION.md) | Entender objetivo de produto, publico e escopo do MVP. |
| [05_SYSTEM_ARCHITECTURE.md](05_SYSTEM_ARCHITECTURE.md) | Entender arquitetura, camadas, dados e fluxos tecnicos. |
| [06_BACKEND_FLASK_API_CONTRACT.md](06_BACKEND_FLASK_API_CONTRACT.md) | Consultar contrato REST, convencoes de erro e gaps de contrato. |
| [29_ENV_EXAMPLE.md](29_ENV_EXAMPLE.md) | Configurar variaveis de ambiente locais e de producao. |
| [30_MAKEFILE_COMMANDS.md](30_MAKEFILE_COMMANDS.md) | Operar instalacao, testes, build e ambiente local. |
| [33_IMPLEMENTATION_STATUS.md](33_IMPLEMENTATION_STATUS.md) | Ver o que esta implementado, testado e pendente. |
| [34_CODEBASE_AUDIT.md](34_CODEBASE_AUDIT.md) | Ler achados de arquitetura, seguranca, qualidade e operacao. |
| [35_TECH_DECISIONS_TRADEOFFS.md](35_TECH_DECISIONS_TRADEOFFS.md) | Entender por que cada tecnologia foi escolhida e seus tradeoffs. |
| [36_IMPROVEMENT_ROADMAP.md](36_IMPROVEMENT_ROADMAP.md) | Priorizar fixes e evolucoes por impacto. |

## Resumo executivo

MindSight AI e um monorepo com backend Flask e frontend React/Vite. A aplicacao entrega um assistente de chat focado em Python, biblioteca local de livros, anexos, busca semantica demonstrativa e integracoes opcionais com OpenAI, Hugging Face e LangSmith.

O projeto esta bem estruturado para um MVP/teste tecnico: ha separacao de rotas, servicos e repositorios no backend; o frontend isola cliente HTTP, componentes de chat e hooks; e existe uma suite relevante de testes unitarios.

Os principais gaps para evoluir de MVP local para produto operavel sao:

- Autenticacao/autorizacao e ownership de dados.
- Uso de servidor WSGI em producao; `run.py` ja exige `FLASK_DEBUG=true` para ligar debug.
- Migracoes versionadas em vez de `db.create_all()` e `ALTER TABLE` no startup.
- Hardening de uploads e transacionalidade de anexos; a delecao de sessao ja remove arquivos fisicos vinculados.
- Paginacao, rate limit e timeouts explicitos para chamadas LLM.
- Contrato OpenAPI alinhado ao comportamento real.
- Observabilidade com request id gerado, logs estruturados e metricas.
- Refatoracao do `frontend/src/App.tsx`, hoje concentrando muitas responsabilidades.

## Estado da auditoria

Auditoria feita em 2026-07-03, considerando o estado local do workspace. Havia mudancas locais preexistentes em `.gitignore`, `backend/app/config.py`, `backend/app/services/observability.py` e arquivos novos de execucao; essas mudancas foram preservadas.

Verificacoes executadas:

- Backend: `ruff check app tests` passou.
- Backend: `compileall app` passou.
- Frontend: `pnpm typecheck` passou.
- Frontend: `pnpm lint` passou.
- Frontend: `pnpm test` passou com 9 arquivos e 64 testes.
- Backend pytest foi tentado, mas no sandbox falhou no setup por permissao de criacao de diretorio temporario. O comando recomendado e `backend/.venv/Scripts/python.exe -m pytest -q --basetemp <diretorio gravavel>`.
