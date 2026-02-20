import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    app_version: str = "1.0.0"
    mongodb_url: str = os.environ.get("DATABASE_URL", "mongodb://localhost:27017/mydb")
    mongodb_name: str = os.environ.get("DATABASE_NAME", "mydb")
    environment: str = os.getenv("ENVIRONMENT", "dev")


def get_settings() -> Settings:
    return Settings()
