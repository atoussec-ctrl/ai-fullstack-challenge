# .env.example

## Backend

```bash
APP_ENV=development
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./storage/app.db

OPENAI_API_KEY=replace-me
OPENAI_MODEL=gpt-4.1-mini

LANGSMITH_TRACING=false
LANGSMITH_API_KEY=replace-me
LANGSMITH_PROJECT=python-ai-assistant

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./storage/faiss.index

UPLOAD_DIR=./storage/uploads
MAX_UPLOAD_SIZE_MB=10

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Frontend

```bash
VITE_API_BASE_URL=http://localhost:5000/api/v1
VITE_APP_NAME=Python AI Assistant
VITE_DEFAULT_THINKING_MODE=balanced
```
