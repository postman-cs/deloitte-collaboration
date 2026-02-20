"""Tests for the /health endpoint."""

import pytest


@pytest.mark.unit
async def test_health_returns_200(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "database" in data
