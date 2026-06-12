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
- [Como clonar](#como-clonar)
- [Configuração de ambiente](#configuração-de-ambiente)
- [Como rodar](#como-rodar)
- [Como testar](#como-testar)
- [API REST](#api-rest)
- [Documentação adicional](#documentação-adicional)
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
│   ├── tests/               # Testes pytest (40 testes)
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

| Ferramenta | Versão mínima |
|------------|---------------|
| Python | 3.12+ |
| Node.js | 20+ (recomendado 24) |
| pnpm | 9+ |
| Git | qualquer versão recente |

**Opcional:**

- Docker e Docker Compose — para subir tudo em containers
- Chave `OPENAI_API_KEY` — para respostas reais da IA
- Chave `HUGGINGFACE_API_KEY` — para modelos DeepSeek via HF
- Chave `LANGSMITH_API_KEY` — para tracing (defina `LANGSMITH_TRACING=true`)

---

## Como clonar

```bash
git clone <url-do-repositorio> mindsight
cd mindsight
```

---

## Configuração de ambiente

1. Copie o template de variáveis de ambiente:

```bash
cp .env.example .env
```

2. Edite `.env` com suas chaves e preferências. Exemplo mínimo para desenvolvimento local **sem** chaves de API:

```bash
APP_ENV=development
CHAT_GATEWAY=local
DATABASE_URL=sqlite:///./storage/app.db
CORS_ALLOWED_ORIGINS=http://localhost:3002,http://127.0.0.1:3002
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=MindSight AI
```

3. Para respostas reais com IA, configure pelo menos uma das opções:

```bash
# OpenAI
OPENAI_API_KEY=sua-chave
OPENAI_MODEL=gpt-4.1-mini
CHAT_GATEWAY=openai

# ou Hugging Face (DeepSeek) — modo auto tenta HF primeiro
HUGGINGFACE_API_KEY=sua-chave
HF_CHAT_MODEL=deepseek-ai/DeepSeek-V4-Flash
CHAT_GATEWAY=auto
```

4. (Opcional) Instale dependências extras de IA/RAG:

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

```bash
docker compose up --build
```

- Frontend: http://localhost:3002
- Backend: http://localhost:5000
- Volume persistente para `backend/storage`

Comandos úteis:

```bash
make docker-down   # parar containers
make docker-logs   # acompanhar logs
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

**Suíte atual:** 40 testes cobrindo health, livros, chat, anexos, busca semântica, OpenAPI, seed, pin/delete de sessões e seleção de gateway.

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

**Suíte atual:** 8 arquivos, 41 testes unitários.

### E2E (Playwright)

```bash
cd frontend
pnpm test:e2e
```

Requer Google Chrome instalado no sistema (configurado com `channel: chrome`).

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

## Licença

Consulte o repositório para informações de licenciamento. Se nenhuma licença estiver definida, o código é disponibilizado apenas para fins educacionais e de avaliação técnica.
