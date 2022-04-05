from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import config
from app.db.uow import UnitOfWork

engine = create_async_engine(config.DATABASE_URI_ASYNC, echo=True, future=True)

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, future=True
)


async def get_uow() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield UnitOfWork(session)
