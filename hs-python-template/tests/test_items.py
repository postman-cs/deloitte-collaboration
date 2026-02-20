"""Tests for the /api/v1/items endpoints."""

import pytest

API_PREFIX = "/api/v1/items"

SAMPLE_ITEM = {
    "name": "Test Widget",
    "description": "A test widget",
    "price": 19.99,
    "quantity": 5,
    "tags": ["test"],
}


@pytest.mark.unit
class TestCreateItem:
    async def test_create_item_returns_201(self, client):
        resp = await client.post(API_PREFIX, json=SAMPLE_ITEM)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == SAMPLE_ITEM["name"]
        assert data["price"] == SAMPLE_ITEM["price"]
        assert "_id" in data

    async def test_create_item_missing_name_returns_422(self, client):
        resp = await client.post(API_PREFIX, json={"price": 10.0})
        assert resp.status_code == 422

    async def test_create_item_negative_price_returns_422(self, client):
        payload = {**SAMPLE_ITEM, "price": -1}
        resp = await client.post(API_PREFIX, json=payload)
        assert resp.status_code == 422


@pytest.mark.unit
class TestListItems:
    async def test_list_items_empty(self, client):
        resp = await client.get(API_PREFIX)
        assert resp.status_code == 200
        data = resp.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_list_items_pagination(self, client):
        # Create 3 items
        for i in range(3):
            await client.post(API_PREFIX, json={**SAMPLE_ITEM, "name": f"Item {i}"})

        resp = await client.get(API_PREFIX, params={"page": 1, "page_size": 2})
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["total"] == 3
        assert data["page"] == 1


@pytest.mark.unit
class TestGetItem:
    async def test_get_existing_item(self, client):
        create_resp = await client.post(API_PREFIX, json=SAMPLE_ITEM)
        item_id = create_resp.json()["_id"]

        resp = await client.get(f"{API_PREFIX}/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == SAMPLE_ITEM["name"]

    async def test_get_nonexistent_item_returns_404(self, client):
        resp = await client.get(f"{API_PREFIX}/507f1f77bcf86cd799439011")
        assert resp.status_code == 404


@pytest.mark.unit
class TestUpdateItem:
    async def test_patch_item(self, client):
        create_resp = await client.post(API_PREFIX, json=SAMPLE_ITEM)
        item_id = create_resp.json()["_id"]

        resp = await client.patch(f"{API_PREFIX}/{item_id}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_patch_nonexistent_returns_404(self, client):
        resp = await client.patch(
            f"{API_PREFIX}/507f1f77bcf86cd799439011",
            json={"name": "Nope"},
        )
        assert resp.status_code == 404


@pytest.mark.unit
class TestDeleteItem:
    async def test_delete_item(self, client):
        create_resp = await client.post(API_PREFIX, json=SAMPLE_ITEM)
        item_id = create_resp.json()["_id"]

        resp = await client.delete(f"{API_PREFIX}/{item_id}")
        assert resp.status_code == 204

        # Verify it's gone
        resp = await client.get(f"{API_PREFIX}/{item_id}")
        assert resp.status_code == 404

    async def test_delete_nonexistent_returns_404(self, client):
        resp = await client.delete(f"{API_PREFIX}/507f1f77bcf86cd799439011")
        assert resp.status_code == 404
