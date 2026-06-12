# Makefile e Comandos

Arquivo: [`Makefile`](../Makefile) na raiz do monorepo.

## Pré-requisitos

- `make`, `python3`, `curl`, `pnpm`
- Ubuntu/Debian: `sudo apt install python3-venv make curl`

Se `python3-venv` não estiver instalado, o target `backend-venv` usa fallback:
`python3 -m venv --without-pip` + bootstrap via `get-pip.py`.

## Instalação

```bash
make install              # backend (.venv) + frontend (pnpm)
make backend-install-ai   # dependências opcionais LangChain/FAISS
```

## Desenvolvimento

```bash
make seed                 # catálogo inicial de livros (idempotente)
make dev                  # backend :5000 + frontend :3002
make backend-dev
make frontend-dev
```

## Docker

```bash
cp .env.example .env      # obrigatório antes do compose
make docker-up            # docker compose up --build
make docker-down
make docker-logs
```

Portas: **5000** (backend), **3002** (frontend).

## Testes

```bash
make test                 # pytest + vitest
make backend-test
make backend-test-cov     # cobertura mínima 85%
make frontend-test
make frontend-test-cov
```

E2E (Playwright, requer Chrome):

```bash
cd frontend && pnpm test:e2e
```

## Qualidade

```bash
make lint
make typecheck
make build
```

## Utilitários

```bash
make db-backup
make db-restore
make clean
```
