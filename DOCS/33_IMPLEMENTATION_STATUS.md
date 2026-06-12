# Status de Implementação

Data: 2026-06-11

## Backend

Implementado em Flask com SQLite e testes automatizados.

### Endpoints disponíveis

- `GET /health`
- `GET /api/v1/health`
- `POST /api/v1/books`
- `POST /api/v1/books/import`
- `GET /api/v1/books?title=&author=`
- `GET /api/v1/books?q=`
- `GET /api/v1/chat/sessions`
- `POST /api/v1/chat/sessions`
- `GET /api/v1/chat/sessions/{session_id}/messages`
- `POST /api/v1/chat/messages`
- `GET /api/v1/chat/messages/{assistant_message_id}/stream`
- `POST /api/v1/chat/messages/{assistant_message_id}/feedback`
- `POST /api/v1/attachments`
- `GET /api/v1/attachments/{attachment_id}`
- `POST /api/v1/semantic-search`
- `GET /openapi.json`
- `GET /docs`

### Arquitetura

- Modelos SQLAlchemy: `Book`, `ChatSession`, `ChatMessage`, `Attachment`.
- Repositórios para persistência de livros e chat.
- Serviços para livros, importação assistida por upload, chat, upload e busca semântica.
- Gateway de IA fakeável em testes e desenvolvimento local.
- Gateway LangChain/OpenAI opcional, carregado de forma lazy.
- Chat usa a biblioteca local como contexto quando a pergunta menciona livros cadastrados.
- LangSmith opcional por `LANGSMITH_TRACING=true`, com traces para chat, importação de livros e busca semântica.
- Feedback de respostas da IA pode ser enviado para LangSmith pelo endpoint de feedback.
- Livros possuem título, categoria, autor, data/ano de publicação e resumo.
- Busca semântica MVP com embeddings locais determinísticos para não depender de downloads no CI.

### Dependências

- `backend/requirements.txt`: runtime core e ferramentas de teste.
- `backend/requirements-ai.txt`: integrações opcionais LangChain/OpenAI/FAISS.
- Instalação deve usar sempre `backend/.venv`.

## Frontend

Implementado em Vite + React + TypeScript com TanStack Query, Tailwind CSS, componentes shadcn-style, Framer Motion e lucide-react.

### Funcionalidades disponíveis

- Layout de chat responsivo inspirado nas referências em `UI_REFERENCE`.
- Tela de administração e consulta de livros.
- Cadastro manual de livros com categoria e ano.
- Importação de livro por upload para extração de título, categoria, autor, ano e resumo.
- Ação para enviar livro cadastrado para a IA resumir/citar usando a base local.
- Sidebar desktop e drawer mobile.
- Histórico de conversas via API.
- Composer fixo no rodapé.
- Envio com `Enter` e quebra de linha com `Shift + Enter`.
- Seletor de modelo.
- Seletor de thinking mode: `fast`, `balanced`, `deep`.
- Tema claro/escuro persistido em `localStorage`.
- Upload de documentos, imagens e áudio com validação local.
- Pré-visualização e remoção de anexos.
- Gravação de áudio via `MediaRecorder`.
- Renderização de Markdown e blocos de código com botão copiar.

## Testes e checks executados

### Backend

```bash
cd backend
.venv/bin/pytest -q
.venv/bin/ruff check app tests
.venv/bin/python -m compileall app
```

Resultado: 11 testes passando.

### Frontend

```bash
cd frontend
pnpm test
pnpm lint
pnpm build
pnpm test:e2e
```

Resultado: 2 arquivos de teste unitário, 4 testes unitários passando, lint e build passando. E2E Playwright com Google Chrome do sistema: 5 testes passando e 1 cenário desktop pulado por ser mobile-only.

## Observações

- O ambiente local não possui `make`, então os targets do `Makefile` não foram executados diretamente; os comandos equivalentes foram validados.
- O `.env` foi sanitizado para não manter token LangSmith real no workspace.
- `langsmith` foi instalado no venv core; dependências pesadas de IA/RAG continuam em `backend/requirements-ai.txt`.
- A porta frontend foi configurada em `3002` porque `5173`, `3000` e `3001` já estavam ocupadas neste ambiente.
- O Playwright usa `channel: chrome` porque o instalador de browsers do Playwright não suporta `ubuntu26.04-x64` neste ambiente.
- Docker Compose foi adicionado para subir backend e frontend juntos.
