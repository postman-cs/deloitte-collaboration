# Contributing to HS Python App

We're thrilled that you're interested in contributing to our project! This document outlines the process and guidelines for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Database](#database)
- [Code Style](#code-style)
- [API Development Workflow](#api-development-workflow)
- [Submitting Changes](#submitting-changes)
- [Testing](#testing-the-application)
- [Building](#building-the-application)
- [Logging](#logging)
- [Secrets & Credentials](#secrets--credentials)
- [Reporting Issues](#reporting-issues)

## Getting Started

### GitHub CodeSpace (Recommended)

You have the option to use [GitHub Codespaces](https://docs.github.com/en/codespaces/getting-started/quickstart) for development on this repository. Codespaces provides a fully-featured, cloud-hosted dev environment that spins up in seconds directly within GitHub, eliminating the need to configure your local setup.

The devcontainer automatically provisions:

- Python 3.13 with uv
- MongoDB 7 instance
- Node.js (for Newman/Postman CLI)
- All VS Code extensions (Ruff, MongoDB, Postman, etc.)

### Local Development

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Deloitte-US-Hosting-Services/hs-python-template.git
    ```

2. **Set Up the Development Environment**:

    ```bash
    # Install uv (https://docs.astral.sh/uv/)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Install all dependencies + pre-commit hooks
    make dev

    # Copy env file
    cp .env.example .env
    ```

3. **Start MongoDB**:

    ```bash
    docker compose up mongo -d
    ```

### Running the Application

```bash
make run
```

On a GitHub Codespace, navigate to `https://<codespace-forwarded-address-8000>/docs`.

On your local machine, navigate to `http://localhost:8000/docs`.

## Database

We use MongoDB with **Beanie** (an async ODM built on Pydantic). The GitHub Codespace configures a local MongoDB instance automatically.

**Connecting:**

- MongoDB URI: `mongodb://localhost:27017`
- Use the [MongoDB VS Code Plugin](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) or `mongosh`:

```bash
mongosh mongodb://localhost:27017
use hs_python_app
db.items.find()
```

**Adding new models:**

1. Create a Beanie `Document` class in `src/app/models/`
2. Create corresponding Pydantic schemas in `src/app/schemas/`
3. Register the model in `src/app/db/__init__.py` → `DOCUMENT_MODELS`
4. Add a service layer in `src/app/services/`
5. Add a router in `src/app/routers/` and include it in `main.py`

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting. Configuration lives in `pyproject.toml`.

```bash
make lint     # Check for issues
make format   # Auto-fix formatting + imports
```

Pre-commit hooks run automatically on every commit if you ran `make dev`.

## API Development Workflow

We follow a **spec-aware** development approach:

1. **Build your FastAPI endpoint** with proper type hints and Pydantic models
2. **Generate the OpenAPI spec**: `make openapi`
3. **Update the Postman collection** if needed: `make postman-collection`
4. **Run contract tests**: `make postman-newman`
5. **Commit** the updated spec and collection with your code changes

The CI pipeline will:

- Lint your OpenAPI spec with `postman api lint` (governance rules)
- Run Newman contract tests against a live instance
- Sync the updated spec to the Postman workspace on merge

## Submitting Changes

1. **Create a Branch**:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. **Commit Your Changes**:

    ```bash
    git add .
    git commit -m "feat: your feature description"
    ```

3. **Push to GitHub**:

    ```bash
    git push origin feature/your-feature-name
    ```

4. **Open a Pull Request**: Use the PR template and ensure all checklist items are addressed.

## Testing the Application

We use [pytest](https://docs.pytest.org/) with `pytest-asyncio` and `httpx` for async testing.

```bash
make test           # Unit tests (uses mongomock, no real DB needed)
make test-cov       # Unit tests with coverage report
make test-integration  # Integration tests (requires running MongoDB)
```

**Writing tests:**

- Place tests in `tests/`
- Use the `client` fixture from `conftest.py` for HTTP tests
- Mark integration tests with `@pytest.mark.integration`
- Aim for ≥80% coverage (enforced in CI)

## Building the Application

Building the app is done automatically with [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) when a pull request is merged to the main branch.

To test locally:

```bash
make build
docker compose up
```

## Deploying the Application

On merge to main, GitHub Actions will:

1. Build a multi-stage Docker image
2. Push it to the [GitHub Container Registry](https://docs.github.com/en/packages/guides/about-github-container-registry)
3. Run Newman contract tests against the built image
4. Sync the OpenAPI spec to Postman Cloud

## Logging

We use [structlog](https://www.structlog.org/) for structured logging:

- **Development**: Pretty-printed, coloured console output
- **Production**: JSON-formatted logs (machine-parseable)

```python
import structlog
logger = structlog.get_logger()

await logger.ainfo("item_created", item_id=str(item.id), name=item.name)
```

## Secrets & Credentials

**Never commit secrets.** This repo has multiple layers of protection:

1. **`.env` is gitignored** — use `.env.example` as a reference
2. **`detect-secrets`** pre-commit hook scans for leaked credentials
3. **Custom Postman env guard** blocks real values in environment files
4. **TruffleHog** runs in CI for verified secrets detection
5. **Postman API keys** go in GitHub Secrets (`POSTMAN_API_KEY`), never in code

If you need to use a secret locally, add it to your `.env` file (which is gitignored).

## Reporting Issues

Use the GitHub issue tracker to report bugs or suggest new features. Before creating a new issue, please check to see if a similar issue already exists.
