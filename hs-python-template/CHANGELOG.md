# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- FastAPI application with health check and example CRUD endpoints
- Pydantic v2 models and schemas with validation
- Beanie ODM integration for MongoDB (async)
- Pydantic Settings for environment configuration
- Structured logging with structlog (JSON in prod, pretty in dev)
- Request logging middleware
- Centralised exception handlers
- Devcontainer setup (Python 3.13 + MongoDB 7 + Node.js)
- GitHub Actions CI pipeline (lint, test, build, secrets scan, API governance)
- GitHub Actions CD pipeline (build, push to GHCR, Newman tests, Postman sync)
- Dependabot for automated dependency updates
- Postman collection with contract tests for all endpoints
- Newman integration for running Postman tests in CI
- Postman CLI API governance in PR checks
- Postman Cloud sync on merge to main
- Pre-commit hooks (ruff, detect-secrets, Postman env guard)
- Multi-stage Dockerfile with non-root user and health check
- docker-compose for local development (app + MongoDB)
- Makefile with common development commands
- VS Code settings, extensions, and debug configurations
- PR template with checklist
- Comprehensive README and CONTRIBUTING docs
