# hs-python-template

Production-ready template for Hosting Services Python APIs built with **FastAPI**, **Pydantic**, **Beanie** (MongoDB), and **uv**.

---

## Quick Start

### GitHub Codespace (Recommended)

Click **Code → Codespaces → New codespace**. The devcontainer will automatically:

- Install Python 3.13 + uv + Node.js
- Spin up a local MongoDB 7 instance
- Install all dependencies and pre-commit hooks

Once ready, start the app:

```bash
make run
# → http://localhost:8000/docs
```

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/Deloitte-US-Hosting-Services/hs-python-template.git
cd hs-python-template

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
make dev

# 4. Copy environment file
cp .env.example .env

# 5. Start MongoDB (Docker)
docker compose up mongo -d

# 6. Run the app
make run
```

Navigate to `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Project Structure

```text
├── .devcontainer/          # GitHub Codespace / devcontainer config
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   ├── Dockerfile.dev
│   └── post-create.sh
├── .github/
│   ├── workflows/
│   │   ├── ci.yml          # Lint → Test → Build on every PR
│   │   └── cd.yml          # Build → Push → Newman → Postman sync on merge
│   ├── dependabot.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── api/                # Generated OpenAPI spec
│   └── postman/            # Postman collection & environments
├── scripts/
│   ├── generate_openapi.py # Export OpenAPI from FastAPI
│   └── check_postman_env.py# Pre-commit secrets guard
├── src/
│   └── app/
│       ├── main.py         # FastAPI application factory
│       ├── config.py       # Pydantic Settings (env vars)
│       ├── db/             # MongoDB connection (Motor + Beanie)
│       ├── models/         # Beanie document models
│       ├── schemas/        # Pydantic request/response schemas
│       ├── routers/        # API route handlers
│       ├── services/       # Business logic layer
│       ├── middleware/      # Request logging, etc.
│       └── exceptions/     # Centralised error handlers
├── tests/                  # Pytest test suite
├── pyproject.toml          # Project config (deps, ruff, pytest)
├── Dockerfile              # Multi-stage production image
├── docker-compose.yml      # Local dev stack (app + MongoDB)
├── Makefile                # Common commands
└── .pre-commit-config.yaml # Git hooks (ruff, secrets detection)
```

---

## Common Commands

| Command | Description |
| --- | --- |
| `make dev` | Install all dependencies + pre-commit hooks |
| `make run` | Start the dev server with hot reload |
| `make lint` | Run Ruff linter |
| `make format` | Auto-format code |
| `make test` | Run unit tests |
| `make test-cov` | Run tests with coverage report |
| `make test-integration` | Run integration tests (requires MongoDB) |
| `make build` | Build the Docker image |
| `make openapi` | Generate OpenAPI spec from the app |
| `make postman-collection` | Generate Postman collection from OpenAPI |
| `make postman-newman` | Run Postman contract tests with Newman |

---

## API Lifecycle & Postman Integration

This template supports a fully automated API lifecycle:

1. **Spec-first**: Define or generate your OpenAPI spec → `docs/api/openapi.json`
2. **Collection sync**: Auto-generate a Postman collection from the spec
3. **Contract testing**: Newman runs the Postman collection in CI against a live app
4. **API governance**: `postman api lint` checks the OpenAPI spec on every PR
5. **Cloud sync**: On merge to main, the updated spec is pushed to your Postman workspace

### Secrets Safety

- **Pre-commit hook** (`detect-secrets`) scans every commit for leaked credentials
- **Custom Postman env guard** blocks commits with real values in environment files
- **TruffleHog** runs in CI for verified secrets detection
- Postman environment templates use `{{VARIABLE}}` placeholders — never hardcode values
- Real API keys go in **GitHub Secrets** only (`POSTMAN_API_KEY`, etc.)

---

## Tech Stack

| Layer | Tool |
| --- | --- |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Database | MongoDB (via Beanie ODM + Motor) |
| Package Manager | uv |
| Linting/Formatting | Ruff |
| Testing | pytest + httpx + mongomock-motor |
| CI/CD | GitHub Actions |
| API Testing | Postman / Newman |
| Containerisation | Docker (multi-stage) |
| Logging | structlog (JSON in prod, pretty in dev) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, branching strategy, and PR checklist.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.
