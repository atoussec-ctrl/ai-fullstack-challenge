# OpenAPI e Contratos

## Objetivo

Garantir que frontend e backend compartilhem contratos claros.

## Flask

Usar `flask-smorest` para gerar OpenAPI.

Rotas sugeridas:

```txt
/docs
/openapi.json
```

## FastAPI

Rotas nativas:

```txt
/docs
/redoc
/openapi.json
```

## Geração de tipos TypeScript

Recomendação:

```bash
pnpm add -D openapi-typescript
pnpm openapi-typescript http://localhost:5000/openapi.json -o src/shared/api/schema.ts
```

## Benefícios

- Menos divergência entre frontend e backend.
- Melhor autocomplete.
- Validação de payloads.
- Base para contract tests.

## Contratos críticos

- `POST /books`
- `GET /books`
- `GET /chat/sessions`
- `POST /chat/sessions`
- `GET /chat/sessions/{id}/messages`
- `POST /chat/messages`
- `GET /chat/messages/{id}/stream`
- `POST /attachments`
- `POST /semantic-search`

## Versionamento

Usar prefixo:

```txt
/api/v1
```

Mudanças breaking devem ir para:

```txt
/api/v2
```

## Política de erro

Todos os erros devem seguir:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensagem legível",
    "details": {}
  }
}
```
