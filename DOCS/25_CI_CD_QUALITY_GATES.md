# CI/CD e Quality Gates

## Pipeline principal

```txt
Pull Request
  ↓
Install
  ↓
Lint
  ↓
Typecheck
  ↓
Unit tests
  ↓
Component tests
  ↓
Backend tests
  ↓
Build frontend
  ↓
E2E smoke
  ↓
Coverage report
```

## Frontend checks

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm test:coverage
pnpm build
pnpm test:e2e
```

## Backend checks

```bash
ruff check .
mypy .
pytest --cov=packages --cov=apps
```

## GitHub Actions exemplo

```yaml
name: Fullstack CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/frontend

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          cache-dependency-path: apps/frontend/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test
      - run: pnpm build

  backend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --upgrade pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy .
      - run: pytest --cov=packages --cov=apps
```

## Gate mínimo para merge

- Lint verde.
- Typecheck verde.
- Testes verdes.
- Build frontend verde.
- Sem segredos detectados.
- Coverage acima do mínimo.
