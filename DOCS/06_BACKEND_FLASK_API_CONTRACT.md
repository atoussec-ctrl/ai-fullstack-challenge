# Backend Flask — Contrato REST Principal

## Objetivo

Definir os endpoints que o frontend Vite/React consumirá.

## Base URL

```txt
http://localhost:5000/api/v1
```

## Health

### GET /health

Response:

```json
{
  "status": "ok",
  "service": "python-ai-assistant"
}
```

## Livros

### POST /books

Request:

```json
{
  "title": "Python Fluente",
  "author": "Luciano Ramalho",
  "publication_date": "2015-08-20",
  "summary": "Livro avançado sobre Python."
}
```

Response `201`:

```json
{
  "id": "uuid",
  "title": "Python Fluente",
  "author": "Luciano Ramalho",
  "publication_date": "2015-08-20",
  "summary": "Livro avançado sobre Python."
}
```

### GET /books?title=python&author=luciano

Response `200`:

```json
[
  {
    "id": "uuid",
    "title": "Python Fluente",
    "author": "Luciano Ramalho",
    "publication_date": "2015-08-20",
    "summary": "Livro avançado sobre Python."
  }
]
```

## Sessões de chat

### GET /chat/sessions

Retorna conversas do usuário.

```json
[
  {
    "id": "session_123",
    "title": "Como criar listas em Python",
    "created_at": "2026-06-11T14:21:00Z",
    "updated_at": "2026-06-11T14:25:00Z"
  }
]
```

### POST /chat/sessions

Request:

```json
{
  "title": "Nova conversa"
}
```

Response:

```json
{
  "id": "session_123",
  "title": "Nova conversa"
}
```

## Mensagens

### GET /chat/sessions/{session_id}/messages

Response:

```json
[
  {
    "id": "msg_1",
    "role": "user",
    "content": "Como criar uma lista em Python?",
    "attachments": [],
    "created_at": "2026-06-11T14:21:00Z"
  },
  {
    "id": "msg_2",
    "role": "assistant",
    "content": "Você pode criar uma lista usando colchetes...",
    "created_at": "2026-06-11T14:21:05Z"
  }
]
```

### POST /chat/messages

Pode receber JSON simples ou `multipart/form-data`.

Request JSON:

```json
{
  "session_id": "session_123",
  "content": "Como criar uma lista em Python?",
  "thinking_mode": "balanced"
}
```

Response:

```json
{
  "user_message_id": "msg_user_123",
  "assistant_message_id": "msg_assistant_123",
  "status": "processing"
}
```

## Streaming

### GET /chat/messages/{assistant_message_id}/stream

Response `text/event-stream`:

```txt
event: token
data: {"content":"Você"}

event: token
data: {"content":" pode"}

event: done
data: {"message_id":"msg_assistant_123"}
```

## Attachments

### POST /attachments

Request `multipart/form-data`:

| Campo | Tipo | Descrição |
|---|---|---|
| file | file | documento, imagem ou áudio |
| session_id | string | sessão de chat |
| kind | string | `document`, `image` ou `audio` |

Response:

```json
{
  "id": "att_123",
  "filename": "erro.png",
  "mime_type": "image/png",
  "size": 123456,
  "kind": "image",
  "url": "/api/v1/attachments/att_123"
}
```

## Thinking modes

| Valor | Uso |
|---|---|
| fast | Resposta rápida e objetiva |
| balanced | Equilíbrio entre velocidade e detalhe |
| deep | Resposta mais analítica e detalhada |

## Erros padronizados

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Campo title é obrigatório.",
    "details": {
      "field": "title"
    }
  }
}
```
