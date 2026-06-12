# Backend FastAPI — Paridade de Funcionalidades

## Objetivo

Manter uma versão FastAPI com os mesmos contratos principais da versão Flask.

## Motivo

A solicitação inicial pediu uma versão com Flask e outra com FastAPI. A integração principal do frontend será com Flask, mas FastAPI permanece como alternativa documentada.

## Endpoints equivalentes

| Funcionalidade | Flask | FastAPI |
|---|---|---|
| Health | `GET /api/v1/health` | `GET /api/v1/health` |
| Criar livro | `POST /api/v1/books` | `POST /api/v1/books` |
| Buscar livros | `GET /api/v1/books` | `GET /api/v1/books` |
| Criar sessão | `POST /api/v1/chat/sessions` | `POST /api/v1/chat/sessions` |
| Listar mensagens | `GET /api/v1/chat/sessions/{id}/messages` | `GET /api/v1/chat/sessions/{id}/messages` |
| Enviar mensagem | `POST /api/v1/chat/messages` | `POST /api/v1/chat/messages` |
| Streaming | `GET /api/v1/chat/messages/{id}/stream` | `GET /api/v1/chat/messages/{id}/stream` |
| Upload | `POST /api/v1/attachments` | `POST /api/v1/attachments` |

## Diferenças

### Flask

- Usa `flask-smorest`.
- Usa Marshmallow para schemas.
- Requer configuração explícita de OpenAPI.

### FastAPI

- Usa Pydantic.
- Gera OpenAPI automaticamente.
- Documentação nativa em `/docs` e `/redoc`.

## Regra

A lógica de negócio não deve ser duplicada entre Flask e FastAPI.

```txt
Flask Blueprint       FastAPI Router
       ↓                    ↓
     Use Cases compartilhados
       ↓
     Domain + Infrastructure
```

## Testes

- Os testes de domínio devem ser compartilhados.
- Os testes de endpoint devem existir para os dois frameworks.
- Testes de contrato devem garantir equivalência de payloads.
