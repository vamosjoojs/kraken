from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import config
from app.db.uow import UnitOfWork

engine = create_async_engine(config.DATABASE_URI_ASYNC, echo=True, future=True)


async def get_uow():
    session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield UnitOfWork(session)
    finally:
        await session.close()
        await engine.dispose()
