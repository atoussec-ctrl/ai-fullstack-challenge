# Python AI Assistant — Fullstack Documentation v3

## Objetivo

Criar uma aplicação fullstack semelhante a uma interface moderna de chat com IA, inspirada nas imagens de referência anexadas pelo usuário, mas com identidade própria.

O assistente será focado em programação Python e deverá atender aos requisitos da prova backend:

1. API de biblioteca virtual.
2. Chatbot com IA generativa usando LangChain, LangSmith e OpenAI.
3. Busca semântica com embeddings e vector store.
4. Frontend moderno com experiência similar a aplicações de chat com IA.
5. Comunicação do frontend com API RESTful em Flask.

## Escopo do pacote

Este pacote contém documentação técnica para:

- backend Flask;
- backend FastAPI como implementação alternativa/paralela;
- chatbot focado em Python;
- embeddings e busca semântica;
- frontend Vite + React + TypeScript;
- testes com Vitest, React Testing Library e Playwright;
- Storybook;
- shadcn/ui;
- Tailwind CSS;
- Motion/Framer Motion;
- TanStack Query, Router e Form;
- uploads de áudio, imagens e documentos;
- tema claro e escuro;
- seletor de modo de raciocínio;
- CI/CD;
- segurança;
- observabilidade;
- roadmap;
- tasks.

## Stack principal

```txt
Frontend:
React + Vite + TypeScript
Tailwind CSS
shadcn/ui
Motion / Framer Motion
TanStack Query
TanStack Router
TanStack Form
Zod
Vitest
React Testing Library
Playwright
Storybook
MSW

Backend:
Python 3.12+
Flask
Flask-Smorest
SQLAlchemy
SQLite
LangChain
LangSmith
OpenAI
FAISS
Sentence Transformers
pytest
Ruff
mypy
```

## Decisão importante

O backend Flask será o alvo principal de integração do frontend.

A versão FastAPI continua documentada como implementação alternativa e para manter compatibilidade com a solicitação inicial, mas a jornada principal de produto será:

```txt
Frontend Vite/React/TypeScript
        ↓
REST API Flask
        ↓
Application Services
        ↓
LangChain / OpenAI / FAISS / SQLite
```

## Comandos iniciais sugeridos

```bash
# frontend
pnpm create vite frontend --template react-ts
cd frontend
pnpm install

# backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Definition of Done

Um módulo só será considerado pronto quando:

- tiver testes unitários;
- tiver testes de integração quando houver API;
- tiver pelo menos um caso E2E se for fluxo crítico;
- estiver documentado;
- passar no lint;
- passar no typecheck;
- não expuser segredos;
- respeitar Clean Code, SOLID, DRY e KISS;
- for acessível por teclado e leitores de tela quando envolver UI.
