import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import items
from .config import get_settings
from .database import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

settings = get_settings()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up app...")
    app.state.db = await get_db()

    yield

    logger.info("Shutting down app...")
    try:
        # await close_db_connection() - Placeholder for your DB close logic
        pass
    except asyncio.exceptions.CancelledError:
        logger.info("CancelledError exception caught.")


app = FastAPI(
    title=settings.app_name, version=settings.app_version, lifespan=app_lifespan
)

environment = settings.environment
app.debug = True if environment == "dev" else False

app.include_router(items.router)
