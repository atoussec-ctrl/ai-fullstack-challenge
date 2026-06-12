# .env.example

Copie para a raiz do projeto:

```bash
cp .env.example .env
```

## Defaults para primeiro run (sem chaves de API)

O template já vem pronto para desenvolvimento local:

```bash
CHAT_GATEWAY=local
OPENAI_API_KEY=
HUGGINGFACE_API_KEY=
LANGSMITH_API_KEY=
```

Com isso o chat usa o gateway determinístico `LocalPythonAssistantGateway`, sem chamadas externas.

Placeholders como `replace-me` são **ignorados** pelo backend quando `CHAT_GATEWAY=auto`.

## Backend

```bash
APP_ENV=development
LOG_LEVEL=INFO
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///./storage/app.db

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
CHAT_GATEWAY=local

HUGGINGFACE_API_KEY=
HF_CHAT_MODEL=deepseek-ai/DeepSeek-V4-Flash
HF_BASE_URL=https://router.huggingface.co/v1

LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=mindsight-ai

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./storage/faiss.index

UPLOAD_DIR=./storage/uploads
MAX_UPLOAD_SIZE_MB=10

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3002,http://127.0.0.1:3002,http://localhost:5000
```

## Frontend

```bash
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=MindSight AI
VITE_DEFAULT_THINKING_MODE=balanced
```

## IA real

```bash
# OpenAI
OPENAI_API_KEY=sua-chave-real
CHAT_GATEWAY=openai

# Hugging Face (DeepSeek)
HUGGINGFACE_API_KEY=sua-chave-real
CHAT_GATEWAY=auto
```
