# ═══════════════════════════════════════════════════════════
# MindSight AI — Makefile
# ═══════════════════════════════════════════════════════════

BACKEND_VENV := backend/.venv
BACKEND_PY := $(BACKEND_VENV)/bin/python
BACKEND_PYTEST := $(BACKEND_VENV)/bin/pytest
BACKEND_RUFF := $(BACKEND_VENV)/bin/ruff
BACKEND_PIP := python3 -m pip --python $(BACKEND_VENV)

.PHONY: install backend-venv backend-install backend-install-ai dev backend-dev frontend-dev docker-up docker-down docker-logs test lint typecheck build clean backend-test backend-test-cov frontend-test frontend-test-cov

# ── Install ──
install: backend-install
	@echo "Installing frontend dependencies..."
	cd frontend && pnpm install
	@echo "All core dependencies installed"

backend-venv:
	test -x $(BACKEND_PY) || python3 -m venv $(BACKEND_VENV)

backend-install: backend-venv
	@echo "Installing backend dependencies into $(BACKEND_VENV)..."
	cd backend && python3 -m pip --python .venv install -r requirements.txt

backend-install-ai: backend-venv
	@echo "Installing optional AI dependencies into $(BACKEND_VENV)..."
	cd backend && python3 -m pip --python .venv install -r requirements-ai.txt

# ── Development ──
backend-dev:
	cd backend && .venv/bin/python run.py

frontend-dev:
	cd frontend && pnpm dev

dev:
	@echo "🚀 Starting MindSight AI..."
	$(MAKE) backend-dev & $(MAKE) frontend-dev

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

# ── Tests ──
backend-test:
	cd backend && .venv/bin/pytest -v --tb=short

backend-test-cov:
	cd backend && .venv/bin/pytest --cov=app --cov-report=term-missing --cov-fail-under=80 -v

frontend-test:
	cd frontend && pnpm test

frontend-test-cov:
	cd frontend && pnpm test -- --coverage

test: backend-test frontend-test

# ── Quality ──
lint:
	cd backend && .venv/bin/ruff check .
	cd frontend && pnpm lint

typecheck:
	cd backend && .venv/bin/python -m compileall app
	cd frontend && pnpm typecheck

# ── Build ──
build:
	cd frontend && pnpm build

# ── Clean ──
clean:
	rm -rf backend/storage/app.db
	rm -rf backend/storage/faiss.index
	rm -rf backend/storage/uploads/*
	rm -rf frontend/dist
	rm -rf frontend/node_modules
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
