from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models import Item, CreateItem
from ..database import get_db

router = APIRouter()


@router.get("/")
async def get_root():
    return {"message": "Welcome! Navigate to /docs for the API documentation."}


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)) -> Item:
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    item["id"] = str(item["_id"])
    del item["_id"]
    return Item(**item)


@router.post("/items", status_code=201, response_model=Item)
async def create_item(
    item: CreateItem, db: AsyncIOMotorDatabase = Depends(get_db)
) -> Item:
    result = await db.items.insert_one(item.model_dump())
    if not result.inserted_id:
        raise HTTPException(
            status_code=500, detail="Failed to create the example item."
        )
    created_item = await db.items.find_one({"_id": result.inserted_id})
    created_item["id"] = str(created_item["_id"])
    del created_item["_id"]
    return Item(**created_item)
