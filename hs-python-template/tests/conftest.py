"""Shared pytest fixtures.

Uses mongomock-motor so unit tests run without a real MongoDB instance.
Integration tests that need a live database should be marked with
`@pytest.mark.integration` and are skipped when no MongoDB is available.
"""

import pytest
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from src.app.db import DOCUMENT_MODELS
from src.app.main import app


@pytest.fixture
async def mock_db():
    """Initialise Beanie with an in-memory mock database."""
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client["test_db"],
        document_models=DOCUMENT_MODELS,
    )
    yield client
    client.close()


@pytest.fixture
async def client(mock_db) -> AsyncClient:
    """Async HTTP test client wired to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
