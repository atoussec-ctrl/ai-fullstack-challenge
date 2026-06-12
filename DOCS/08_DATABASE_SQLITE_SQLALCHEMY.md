# Banco de Dados — SQLite + SQLAlchemy

## Objetivo

Atender à exigência da prova de usar SQLite e manter uma arquitetura preparada para migração futura.

## Entidades persistidas no MVP

### Book

| Campo | Tipo |
|---|---|
| id | UUID string |
| title | string |
| author | string |
| publication_date | date |
| summary | text |
| created_at | datetime |

### ChatSession

| Campo | Tipo |
|---|---|
| id | string |
| title | string |
| created_at | datetime |
| updated_at | datetime |

### Message

| Campo | Tipo |
|---|---|
| id | string |
| session_id | string |
| role | user/assistant/system |
| content | text |
| thinking_mode | string |
| status | pending/streaming/completed/error |
| created_at | datetime |

### Attachment

| Campo | Tipo |
|---|---|
| id | string |
| message_id | string |
| filename | string |
| mime_type | string |
| size | int |
| kind | document/image/audio |
| storage_path | string |
| created_at | datetime |

## Repositórios

```python
class BookRepository:
    def create(self, book):
        raise NotImplementedError

    def search(self, title=None, author=None):
        raise NotImplementedError
```

## Testes

- Repositório deve ser testado com SQLite temporário.
- Cada teste deve iniciar banco limpo.
- Não usar banco real de desenvolvimento em testes.

## Evolução

- PostgreSQL para produção.
- Alembic para migrations.
- Storage externo para anexos.
- Índices em `session_id`, `author`, `title`.
