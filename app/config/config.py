import logging
import os

from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    API_PREFIX = "/api"
    
    DEBUG: Optional[bool] = None
    
    VERSION = "0.1.1"
    
    PROJECT_NAME: Optional[str] = "FastAPI example application"
    
    ENV: Optional[str] = "Local"
    
    LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    
    DATABASE_URI_ASYNC: Optional[str] = None
    
    REDIS_URL: Optional[str] = None
    RABBITMQ_DEFAULT_QUEUE_NAME: Optional[str] = None

    INSTA_USERNAME: Optional[str] = None
    INSTA_PASSWORD: Optional[str] = None

    TWITCH_APP_ID: Optional[str] = None
    TWITCH_APP_SECRET: Optional[str] = None

    @classmethod
    def db_fields(cls):
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        db = os.getenv('POSTGRES_DB')
        port = os.getenv('POSTGRES_PORT', 5432)
        return user, password, host, db, port

    @validator("DATABASE_URI_ASYNC", pre=True)
    def assemble_async_db_connection(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v

        user, password, host, db, port = cls.db_fields()
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    class Config:
        env_file = ".env"


config = Settings()
