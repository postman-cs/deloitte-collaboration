.PHONY: help install dev lint format test test-cov test-integration run build openapi postman-collection postman-newman clean

PYTHON := uv run

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────

install: ## Install production dependencies
	uv sync

dev: ## Install all dependencies (including dev)
	uv sync --extra dev
	$(PYTHON) pre-commit install

# ── Code quality ─────────────────────────────────────────────────────

lint: ## Run linter (ruff check)
	$(PYTHON) ruff check .

format: ## Format code (ruff format)
	$(PYTHON) ruff format .
	$(PYTHON) ruff check . --fix

# ── Testing ──────────────────────────────────────────────────────────

test: ## Run unit tests
	$(PYTHON) pytest -m "unit or not integration"

test-cov: ## Run tests with coverage report
	$(PYTHON) pytest --cov --cov-report=html --cov-report=term-missing -m "unit or not integration"

test-integration: ## Run integration tests (requires MongoDB)
	$(PYTHON) pytest -m integration

# ── Application ──────────────────────────────────────────────────────

run: ## Start the development server
	$(PYTHON) uvicorn src.app.main:app --host 127.0.0.1 --port 8000 --reload

build: ## Build the Docker image
	docker build -t hs-python-app .

# ── API Documentation ────────────────────────────────────────────────

openapi: ## Generate the OpenAPI spec from FastAPI
	$(PYTHON) python scripts/generate_openapi.py

postman-collection: openapi ## Generate Postman collection from OpenAPI spec
	npx openapi-to-postmanv2 -s docs/api/openapi.json -o docs/postman/collection.generated.json -p

postman-newman: ## Run the Postman collection with Newman
	newman run docs/postman/collection.json \
		--environment docs/postman/environment.local.json \
		--reporters cli

# ── Cleanup ──────────────────────────────────────────────────────────

clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache htmlcov coverage.xml .coverage dist build *.egg-info
