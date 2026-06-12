# MindSight AI

Assistente fullstack de chat com IA focado em **Python**, com biblioteca virtual de livros, busca semântica e interface moderna inspirada em aplicações de chat com IA.

O projeto atende aos requisitos de uma prova backend: API REST em Flask, chatbot com LangChain/LangSmith/OpenAI, embeddings com vector store e frontend React consumindo a API.

---

## Índice

- [Visão geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Stack tecnológica](#stack-tecnológica)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Quick Start](#quick-start)
- [Como clonar](#como-clonar)
- [Configuração de ambiente](#configuração-de-ambiente)
- [Como rodar](#como-rodar)
- [Como testar](#como-testar)
- [API REST](#api-rest)
- [Documentação adicional](#documentação-adicional)
- [Utilitários](#utilitários)
- [Solução de problemas](#solução-de-problemas)
- [Licença](#licença)

---

## Visão geral

**MindSight AI** é um monorepo com backend Flask e frontend Vite/React. O assistente responde perguntas sobre programação Python, usa a biblioteca local de livros como contexto quando relevante, aceita anexos (documentos, imagens e áudio) e persiste conversas em SQLite.

O gateway de IA suporta três modos de operação:

| Modo | Descrição |
|------|-----------|
| `local` | Respostas determinísticas — ideal para desenvolvimento e CI, sem chave de API |
| `openai` | Integração com modelos OpenAI via LangChain |
| `auto` | Prioriza Hugging Face (DeepSeek) → OpenAI → fallback local |

---

## Funcionalidades

### Chat com IA

- Conversas com histórico persistido por sessão
- Streaming de respostas via Server-Sent Events (SSE)
- Modos de raciocínio: **rápido**, **equilibrado** e **profundo**
- Seleção de modelo (OpenAI, DeepSeek via Hugging Face, etc.)
- Renderização de Markdown com blocos de código e botão copiar
- Feedback de respostas integrado ao LangSmith (opcional)
- Fixar/desafixar conversas na sidebar
- Exclusão de sessões (incluindo gesto swipe no mobile)

### Biblioteca virtual

- Cadastro manual de livros (título, categoria, autor, ano, resumo)
- Importação de livros por upload (PDF, TXT, Markdown) com extração assistida
- Busca por título, autor, categoria ou texto livre
- Contexto de livros injetado automaticamente no chat quando a pergunta menciona o acervo

### Busca semântica

- Endpoint `POST /api/v1/semantic-search` com embeddings e FAISS
- Embeddings locais determinísticos no CI; modelos reais opcionais via `requirements-ai.txt`

### Anexos

- Upload de documentos, imagens e áudio
- Gravação de áudio via `MediaRecorder` no navegador
- Validação de tipo e tamanho no frontend e backend
- Texto extraído de anexos usado como contexto na resposta da IA

### Interface

- Layout responsivo (desktop, tablet e mobile)
- Sidebar com agrupamento de sessões e drawer no mobile
- Tema claro/escuro persistido em `localStorage`
- Tela de administração de livros
- Animações com Framer Motion

---

## Arquitetura

```
Usuário
  ↓
Frontend (React + Vite + TypeScript)
  ↓ REST / SSE
Backend Flask (API /api/v1)
  ↓
Serviços de aplicação (chat, livros, uploads, busca semântica)
  ↓
Infraestrutura
  ├── SQLite (SQLAlchemy)
  ├── OpenAI / Hugging Face (LangChain)
  ├── LangSmith (tracing opcional)
  └── FAISS (vector store)
```

**Modelos de dados:** `Book`, `ChatSession`, `ChatMessage`, `Attachment`

**Camadas backend:**

- `routes/` — blueprints Flask (HTTP)
- `services/` — regras de negócio e gateways de IA
- `repositories.py` — persistência
- `models.py` — entidades SQLAlchemy

**Frontend:**

- `App.tsx` — shell principal (chat, livros, configurações)
- `features/chat/` — componentes e hooks do chat
- `shared/api/` — cliente HTTP e tipos
- `components/ui/` — componentes base (estilo shadcn/ui)

---

## Stack tecnológica

### Backend

| Tecnologia | Uso |
|------------|-----|
| Python 3.12+ | Runtime |
| Flask 3.x | Framework web |
| Flask-SQLAlchemy | ORM |
| SQLite | Banco de dados |
| Marshmallow | Validação/serialização |
| LangChain + LangChain-OpenAI | Integração com LLMs |
| LangSmith | Tracing e feedback |
| OpenAI API | Modelos GPT |
| Hugging Face Inference | DeepSeek e modelos compatíveis |
| FAISS + Sentence Transformers | Busca semântica (opcional) |
| pypdf | Extração de texto de PDFs |
| pytest + Ruff | Testes e lint |

### Frontend

| Tecnologia | Uso |
|------------|-----|
| React 19 | UI |
| TypeScript 6 | Tipagem |
| Vite 8 | Build e dev server |
| Tailwind CSS 4 | Estilos |
| TanStack Query | Estado servidor / cache |
| Framer Motion | Animações |
| react-markdown + remark-gfm | Renderização Markdown |
| Zod | Validação |
| Vitest + Testing Library | Testes unitários |
| Playwright | Testes E2E |
| Storybook | Documentação de componentes |
| lucide-react | Ícones |

### DevOps

| Tecnologia | Uso |
|------------|-----|
| Docker Compose | Orquestração local |
| Makefile | Automação de tarefas |

---

## Estrutura do repositório

```
mindsight/
├── backend/
│   ├── app/
│   │   ├── routes/          # Endpoints REST
│   │   ├── services/        # Lógica de negócio
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   ├── repositories.py  # Acesso a dados
│   │   └── config.py        # Configurações por ambiente
│   ├── tests/               # Testes pytest (41 testes)
│   ├── storage/             # SQLite, uploads, índice FAISS
│   ├── requirements.txt     # Dependências core
│   ├── requirements-ai.txt  # Dependências opcionais de IA/RAG
│   ├── run.py               # Entry-point do servidor
│   └── seed.py              # Seed do catálogo de livros
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Aplicação principal
│   │   ├── features/        # Módulos de funcionalidade
│   │   ├── shared/          # API client, utils, tipos
│   │   └── components/ui/   # Componentes base
│   ├── e2e/                 # Testes Playwright
│   └── package.json
├── DOCS/                    # Documentação técnica detalhada
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

---

## Pré-requisitos

| Ferramenta | Versão mínima | Observação |
|------------|---------------|------------|
| Python | 3.12+ | Com suporte a `venv` |
| Node.js | 20+ (recomendado 24) | Inclui Corepack para `pnpm` |
| pnpm | 9+ | `corepack enable` se o comando não existir |
| Make | 4+ | Automação dos comandos abaixo |
| Git | recente | Clone e versionamento |
| curl | recente | Fallback do Makefile para bootstrap do pip |

**Ubuntu/Debian — pacote do venv (recomendado):**

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip make curl
# Use a versão do Python instalada, por exemplo:
# sudo apt install -y python3.12-venv
```

Sem `python3-venv`, o `make install` ainda tenta um fallback (`venv --without-pip` + `get-pip.py`), mas instalar o pacote acima é mais simples.

**Opcional:**

- Docker e Docker Compose — ambiente containerizado
- Google Chrome — exigido pelos testes E2E do Playwright (`channel: chrome`)
- Chave `OPENAI_API_KEY` — respostas reais via OpenAI
- Chave `HUGGINGFACE_API_KEY` — modelos DeepSeek via Hugging Face
- Chave `LANGSMITH_API_KEY` — tracing (`LANGSMITH_TRACING=true`)

**Portas usadas localmente:**

| Porta | Serviço |
|-------|---------|
| 5000 | Backend Flask |
| 3002 | Frontend Vite (`strictPort`) |
| 6006 | Storybook (opcional) |

---

## Quick Start

Fluxo mínimo testado em clone limpo — funciona **sem chaves de API**:

```bash
git clone https://github.com/atoussec-ctrl/AI_PYTHON_TEST_FULLSTACK.git mindsight
cd mindsight
cp .env.example .env
make install
make seed
make dev
```

Abra http://localhost:3002, envie uma pergunta sobre Python e confirme a resposta.

Verifique o backend:

```bash
curl -s http://localhost:5000/api/v1/health
```

Rodar a suíte de testes:

```bash
make test
```

> O `.env.example` já vem com `CHAT_GATEWAY=local` e chaves vazias. Placeholders como `replace-me` são ignorados pelo backend.

---

## Como clonar

```bash
git clone https://github.com/atoussec-ctrl/AI_PYTHON_TEST_FULLSTACK.git mindsight
cd mindsight
```

---

## Configuração de ambiente

1. Copie o template:

```bash
cp .env.example .env
```

2. Para o **primeiro run**, o `.env.example` já está pronto para desenvolvimento local:
   - `CHAT_GATEWAY=local` — respostas determinísticas, sem API externa
   - chaves de API vazias

3. Para **IA real**, edite `.env`:

```bash
# OpenAI
OPENAI_API_KEY=sua-chave-real
OPENAI_MODEL=gpt-4.1-mini
CHAT_GATEWAY=openai

# ou Hugging Face (DeepSeek) — auto tenta HF -> OpenAI -> local
HUGGINGFACE_API_KEY=sua-chave-real
HF_CHAT_MODEL=deepseek-ai/DeepSeek-V4-Flash
CHAT_GATEWAY=auto
```

4. (Opcional) Dependências extras de IA/RAG:

```bash
make backend-install-ai
```

---

## Como rodar

### Opção 1 — Makefile (recomendado)

Instalar dependências:

```bash
make install
```

Popular o catálogo inicial de livros:

```bash
make seed
```

Subir backend e frontend em paralelo:

```bash
make dev
```

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:3002 |
| Backend API | http://localhost:5000/api/v1 |
| Health check | http://localhost:5000/health |
| OpenAPI / Swagger | http://localhost:5000/docs |

Rodar apenas um serviço:

```bash
make backend-dev   # Flask na porta 5000
make frontend-dev  # Vite na porta 3002
```

### Opção 2 — Manual

**Backend:**

```bash
cd backend
python3 -m venv .venv
python3 -m pip --python .venv install -r requirements.txt
.venv/bin/python run.py
```

**Frontend:**

```bash
cd frontend
pnpm install
pnpm dev
```

O Vite faz proxy de `/api` para `http://localhost:5000` automaticamente.

### Opção 3 — Docker Compose

Requer `.env` na raiz (`cp .env.example .env`). Libere as portas **5000** e **3002** antes de subir.

```bash
docker compose up --build
```

- Frontend: http://localhost:3002
- Backend: http://localhost:5000
- Volume persistente para `backend/storage`

Comandos úteis:

```bash
make docker-down   # parar containers
make docker-logs     # acompanhar logs
```

---

## Como testar

### Todos os testes

```bash
make test
```

### Backend (pytest)

```bash
make backend-test
```

Com cobertura mínima de 85%:

```bash
make backend-test-cov
```

Ou manualmente:

```bash
cd backend
.venv/bin/pytest -v
.venv/bin/ruff check app tests
```

**Suíte atual:** 41 testes backend — health, livros, chat, anexos, busca semântica, OpenAPI, seed, pin/delete de sessões e seleção de gateway.

### Frontend (Vitest)

```bash
make frontend-test
```

Com cobertura:

```bash
make frontend-test-cov
```

Ou manualmente:

```bash
cd frontend
pnpm test          # execução única
pnpm test:watch    # modo watch
pnpm lint
pnpm typecheck
pnpm build
```

**Suíte atual:** 9 arquivos, 43 testes unitários.

### E2E (Playwright)

```bash
cd frontend
pnpm test:e2e
```

Requisitos:

- Google Chrome instalado no sistema (`channel: chrome` no Playwright)
- Porta **3002** livre (o Playwright sobe `pnpm dev` automaticamente)

Resultado esperado: **5 passando**, **1 pulado** (cenário mobile-only no projeto desktop).

### Storybook

```bash
cd frontend
pnpm storybook
```

Abre em http://localhost:6006

### Qualidade geral

```bash
make lint       # Ruff (backend) + ESLint (frontend)
make typecheck  # compileall (backend) + tsc (frontend)
make build      # build de produção do frontend
```

---

## API REST

Base URL: `http://localhost:5000/api/v1`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Health check |
| `POST` | `/books` | Cadastrar livro |
| `POST` | `/books/import` | Importar livro por upload |
| `GET` | `/books` | Listar/buscar livros |
| `GET` | `/books/{id}` | Detalhe de um livro |
| `GET` | `/chat/sessions` | Listar sessões |
| `POST` | `/chat/sessions` | Criar sessão |
| `PATCH` | `/chat/sessions/{id}` | Fixar/desafixar sessão |
| `DELETE` | `/chat/sessions/{id}` | Excluir sessão |
| `GET` | `/chat/sessions/{id}/messages` | Mensagens da sessão |
| `POST` | `/chat/messages` | Enviar mensagem |
| `GET` | `/chat/messages/{id}/stream` | Stream SSE da resposta |
| `POST` | `/chat/messages/{id}/feedback` | Feedback LangSmith |
| `POST` | `/attachments` | Upload de anexo |
| `GET` | `/attachments/{id}` | Download de anexo |
| `POST` | `/semantic-search` | Busca semântica |
| `GET` | `/openapi.json` | Especificação OpenAPI |
| `GET` | `/docs` | Documentação interativa |

Contrato completo em [`DOCS/06_BACKEND_FLASK_API_CONTRACT.md`](DOCS/06_BACKEND_FLASK_API_CONTRACT.md).

---

## Documentação adicional

A pasta [`DOCS/`](DOCS/) contém documentação técnica extensa:

| Documento | Conteúdo |
|-----------|----------|
| [`DOCS/00_README_FULLSTACK.md`](DOCS/00_README_FULLSTACK.md) | Visão geral do pacote de docs |
| [`DOCS/01_PRODUCT_VISION.md`](DOCS/01_PRODUCT_VISION.md) | Visão de produto e personas |
| [`DOCS/05_SYSTEM_ARCHITECTURE.md`](DOCS/05_SYSTEM_ARCHITECTURE.md) | Arquitetura e princípios SOLID |
| [`DOCS/33_IMPLEMENTATION_STATUS.md`](DOCS/33_IMPLEMENTATION_STATUS.md) | Status de implementação |
| [`DOCS/29_ENV_EXAMPLE.md`](DOCS/29_ENV_EXAMPLE.md) | Variáveis de ambiente |
| [`DOCS/30_MAKEFILE_COMMANDS.md`](DOCS/30_MAKEFILE_COMMANDS.md) | Comandos do Makefile |

---

## Utilitários

```bash
make seed         # Popular catálogo de livros (idempotente)
make db-backup    # Backup do SQLite
make db-restore   # Restaurar backup mais recente
make clean        # Limpar storage, dist e caches
```

---

## Solução de problemas

### `make install` falha ao criar o venv

**Sintoma:** `ensurepip is not available`

**Solução:**

```bash
sudo apt install -y python3-venv   # ou python3.12-venv / python3.14-venv
make install
```

O Makefile também tenta automaticamente `venv --without-pip` + bootstrap do pip.

### Chat retorna erro de IA logo após clonar

**Causa comum:** `CHAT_GATEWAY=auto` com chaves placeholder ou inválidas.

**Solução:** use `CHAT_GATEWAY=local` no `.env` (já é o default do `.env.example`).

### Porta 5000 ou 3002 em uso

**Sintoma:** `Address already in use` ou Docker `Bind for 0.0.0.0:5000 failed`

**Solução:**

```bash
ss -tlnp | grep -E ':5000|:3002'
make docker-down    # se houver containers antigos
# pare o processo listado ou encerre outra instância do projeto
```

### `pnpm: command not found`

```bash
corepack enable
corepack prepare pnpm@latest --activate
```

### Frontend sem resposta da API

Confirme que o backend está no ar e que o proxy aponta para a porta correta:

- Backend: http://localhost:5000/api/v1/health
- Dev local: Vite faz proxy de `/api` → `http://localhost:5000`

### Testes E2E falham

Instale o Google Chrome. Se a porta 3002 estiver ocupada, libere-a antes de rodar `pnpm test:e2e`.

---

## Licença

Consulte o repositório para informações de licenciamento. Se nenhuma licença estiver definida, o código é disponibilizado apenas para fins educacionais e de avaliação técnica.
