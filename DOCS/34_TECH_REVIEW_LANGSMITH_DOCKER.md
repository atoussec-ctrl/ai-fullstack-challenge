# Revisão Técnica, Métricas LangSmith e Docker

Data: 2026-06-11

## Revisão por papéis

### Tech Leads / Lead Engineers

- Confirmar que os contratos principais estão versionados em `/api/v1`.
- Confirmar que livros são domínio persistente, não apenas mock de tela.
- Confirmar que chat não inventa dados de livros: ele cita apenas campos cadastrados na base local.
- Próximo refinamento recomendado: separar `App.tsx` em módulos menores após estabilizar os fluxos.

### Backend / AI Engineers

- `ChatService.ask` é traceável via LangSmith quando `LANGSMITH_TRACING=true`.
- `BookImportService.import_file` e `BookMetadataExtractor.extract` são traceáveis.
- `SemanticSearchService.search` é traceável como retriever.
- Gateway LangChain/OpenAI continua lazy para não quebrar testes locais.
- Extração de livro por upload usa heurística determinística no MVP; o contrato permite trocar por LLM depois.

### DBA / Data

- SQLite persiste `books`, `chat_sessions`, `chat_messages` e `attachments`.
- `Book` agora contém título, categoria, autor, data/ano de publicação e resumo.
- Migração leve em runtime adiciona `books.category` e `chat_messages.trace_id` em bancos SQLite antigos.
- Próximo refinamento recomendado: Alembic para migrations formais.

### QA / Automation

- Backend: pytest cobre livros, importação por upload, chat com contexto de livros, anexos, health e busca semântica.
- Frontend: Vitest cobre shell e tela de biblioteca.
- E2E: Playwright cobre shell, tema/thinking, mobile drawer e tela de biblioteca.
- Docker Compose validado por `docker compose config`.

### Security

- `.env` foi sanitizado.
- Upload de anexos e importação de livros validam extensão e tamanho/legibilidade no backend.
- CORS está restrito a origens locais de dev.
- Próximo refinamento recomendado: autenticação/autorização antes de publicar a API fora da rede local.

## Métricas LangSmith

Ativação:

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=replace-me
LANGSMITH_PROJECT=mindsight-ai
```

Traces atuais:

- `chat.ask`: fluxo completo de pergunta, contexto local de livros e resposta.
- `chat.local_python_assistant`: gateway local determinístico.
- `chat.langchain_openai`: gateway LangChain/OpenAI opcional.
- `books.import_file`: importação completa de livro por upload.
- `books.extract_metadata`: extração de título, categoria, autor, ano e resumo.
- `semantic_search.search`: busca semântica local.

Feedback:

```http
POST /api/v1/chat/messages/{assistant_message_id}/feedback
```

Payload:

```json
{
  "score": 1,
  "key": "user_score",
  "comment": "Resposta correta e citou a fonte."
}
```

Score deve ficar entre `-1` e `1`. Se LangSmith estiver desligado ou a mensagem não tiver `trace_id`, o endpoint responde `202` com `recorded=false`, sem quebrar o fluxo do usuário.

Métricas recomendadas para acompanhamento:

- Taxa de respostas com contexto de livros.
- Taxa de feedback positivo/negativo por `thinking_mode`.
- Latência por trace: chat, importação, extração e busca.
- Falhas de extração de livro por motivo: metadados ausentes, extensão inválida, arquivo ilegível.
- Número de livros cadastrados manualmente versus importados.
- Consultas sem livro relevante encontrado.

## Docker

Subir stack:

```bash
docker compose up --build
```

Serviços:

- Backend Flask: `http://localhost:5000`
- Frontend Vite: `http://localhost:3002`

O frontend usa `VITE_API_BASE_URL=/api/v1` e proxy Vite para encaminhar `/api` ao serviço `backend:5000` dentro da rede Docker. Isso evita que navegadores em outros dispositivos tentem chamar `localhost:5000` do próprio dispositivo.

Dados persistentes:

- Volume Docker `backend-storage` montado em `/app/storage`.

Parar stack:

```bash
docker compose down
```
