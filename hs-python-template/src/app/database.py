import logging
from motor.motor_asyncio import AsyncIOMotorClient

# from fastapi import Depends
from .config import get_settings

settings = get_settings()
log = logging.getLogger("uvicorn")


async def get_db() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.mongodb_url)
    return client[settings.mongodb_name]
