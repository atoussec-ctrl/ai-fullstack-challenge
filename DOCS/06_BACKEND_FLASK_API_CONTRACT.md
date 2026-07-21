# Contrato da API Flask

Base URL local: `http://localhost:5000/api/v1`

O backend tambem expoe:

- `GET /health`
- `GET /openapi.json`
- `GET /docs`

## Convencoes

Todas as respostas de erro seguem:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Mensagem legivel.",
    "details": {}
  },
  "request_id": "opcional"
}
```

Campos temporais sao retornados em ISO 8601. IDs sao strings geradas via UUID com prefixo para sessoes, mensagens e anexos.

## Endpoints publicos

| Metodo | Endpoint | Uso |
| --- | --- | --- |
| GET | `/health` | Health check da API versionada. |
| GET | `/books` | Lista/busca livros por titulo, autor, categoria ou `q`. |
| POST | `/books` | Cria livro manualmente. |
| POST | `/books/import` | Importa livro via TXT/MD/JSON/PDF. |
| GET | `/books/{book_id}` | Detalhe de livro. |
| GET | `/chat/sessions` | Lista sessoes de chat. |
| POST | `/chat/sessions` | Cria sessao. |
| PATCH | `/chat/sessions/{session_id}` | Atualiza metadados da sessao, hoje `pinned`. |
| DELETE | `/chat/sessions/{session_id}` | Remove sessao e registros relacionados. |
| GET | `/chat/sessions/{session_id}/messages` | Lista mensagens da sessao. |
| POST | `/chat/messages` | Envia pergunta e cria resposta do assistente. |
| GET | `/chat/messages/{assistant_message_id}/stream` | SSE simulado da mensagem ja persistida. |
| POST | `/chat/messages/{assistant_message_id}/feedback` | Envia feedback para LangSmith, se habilitado. |
| POST | `/attachments` | Upload de anexo para uma sessao. |
| GET | `/attachments/{attachment_id}` | Download de anexo. |
| DELETE | `/attachments/{attachment_id}` | Remove um anexo ainda nao vinculado a uma mensagem (cleanup apos falha no envio). Rejeita anexo ja vinculado. |
| POST | `/semantic-search` | Busca semantica local demonstrativa. |

## Modelos principais

### Book

```json
{
  "id": "book-id",
  "title": "Python Fluente",
  "category": "Programacao",
  "author": "Luciano Ramalho",
  "publication_date": "2015-01-01",
  "publication_year": 2015,
  "summary": "Resumo",
  "created_at": "2026-07-03T00:00:00Z"
}
```

### ChatSession

```json
{
  "id": "session_x",
  "title": "Nova conversa",
  "pinned": false,
  "pinned_at": null,
  "created_at": "2026-07-03T00:00:00Z",
  "updated_at": "2026-07-03T00:00:00Z"
}
```

### ChatMessage

```json
{
  "id": "msg_x",
  "session_id": "session_x",
  "role": "assistant",
  "content": "Resposta",
  "thinking_mode": "balanced",
  "status": "completed",
  "trace_id": null,
  "attachments": [],
  "created_at": "2026-07-03T00:00:00Z"
}
```

## Gaps de contrato encontrados

| Gap | Evidencia | Recomendacao |
| --- | --- | --- |
| Status de falha | Backend, OpenAPI e frontend usam `failed` para falha persistida do assistente. | Manter teste de contrato cobrindo esse enum. |
| OpenAPI e tipos TypeScript sao manuais | `routes/openapi.py` e `shared/api/types.ts` evoluem separadamente. | Gerar tipos do OpenAPI ou testar valores reais contra schema. |
| Sem autenticacao | Todos os endpoints sao publicos no app atual. | Adicionar auth e ownership antes de expor fora do ambiente local. |
| Sem paginacao | Listagens usam `.all()` no backend. | Incluir `limit`, `cursor`/`page` e limites maximos. |
| SSE nao e streaming real | Endpoint emite tokens de mensagem ja persistida. | Migrar para streaming real do gateway ou renomear como playback. |

## Criterios para manter contrato saudavel

- Cada novo endpoint deve ter teste HTTP.
- Cada schema OpenAPI deve refletir payload real serializado.
- O frontend deve consumir tipos gerados ou testados contra fixture do backend.
- Mudancas quebraveis devem ser versionadas em `/api/v2` ou protegidas por compatibilidade.
