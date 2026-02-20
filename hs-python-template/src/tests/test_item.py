import pytest
from fastapi.testclient import TestClient
from bson import ObjectId

from app.main import app
from app.database import get_db


# Mock database
@pytest.fixture
def mock_db(mocker):
    class MockDatabase:
        items = mocker.MagicMock()

    return MockDatabase()


# Override the get_db dependency
@pytest.fixture
def override_get_db(mock_db):
    def _get_db_override():
        return mock_db

    return _get_db_override


# Test client with dependency overrides
@pytest.fixture
def client(override_get_db, mock_db):
    app.dependency_overrides[get_db] = override_get_db
    app.state.db = mock_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    # Clean up mock database
    del app.state.db


# Tests for get_item endpoint
@pytest.mark.asyncio
async def test_get_item(client, mocker):
    test_id = str(ObjectId())
    mock_item = {
        "_id": ObjectId(test_id),
        "name": "test_item",
        "description": "test_description",
    }
    client_items = client.app.state.db.items
    client_items.find_one = mocker.AsyncMock(return_value=mock_item)

    response = client.get(f"/items/{test_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": test_id,
        "name": "test_item",
        "description": "test_description",
    }

    # Test for item not found
    client_items.find_one = mocker.AsyncMock(return_value=None)
    response = client.get(f"/items/{test_id}")
    assert response.status_code == 404


# Tests for create_item endpoint
@pytest.mark.asyncio
async def test_create_item(client, mocker):
    mock_item = {"name": "new_item", "description": "new_description"}
    mock_id = ObjectId()
    client_items = client.app.state.db.items
    client_items.insert_one = mocker.AsyncMock(
        return_value=mocker.Mock(inserted_id=mock_id)
    )
    client_items.find_one = mocker.AsyncMock(return_value={**mock_item, "_id": mock_id})

    response = client.post("/items", json=mock_item)
    assert response.status_code == 201
    assert response.json() == {
        "id": str(mock_id),
        "name": "new_item",
        "description": "new_description",
    }
