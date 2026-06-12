# Makefile e Comandos

## Makefile sugerido

```makefile
.PHONY: install dev test lint typecheck build frontend-dev backend-dev

install:
	cd apps/frontend && pnpm install
	pip install -e ".[dev]"

frontend-dev:
	cd apps/frontend && pnpm dev

backend-dev:
	flask --app apps.backend-flask.src.app:create_app run --debug --port 5000

dev:
	make backend-dev & make frontend-dev

frontend-test:
	cd apps/frontend && pnpm test

frontend-e2e:
	cd apps/frontend && pnpm test:e2e

frontend-storybook:
	cd apps/frontend && pnpm storybook

backend-test:
	pytest

lint:
	cd apps/frontend && pnpm lint
	ruff check .

typecheck:
	cd apps/frontend && pnpm typecheck
	mypy .

build:
	cd apps/frontend && pnpm build
```

## Scripts frontend package.json

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "typecheck": "tsc --noEmit",
    "lint": "eslint ."
  }
}
```
