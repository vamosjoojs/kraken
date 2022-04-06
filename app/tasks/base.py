from celery import Task
from sqlalchemy.ext.asyncio.session import AsyncSession
import asyncio

from app.db.uow import UnitOfWork
from app.api.dependencies.get_db import engine


class DatabaseTask(Task):
    _session = None
    _engine = engine

    async def close_connections(self):
        if self._session is not None:
            await self._session.close()
            await self._engine.dispose()

    def after_return(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close_connections())

    @property
    def get_db(self):
        if self._session is None:
            self._session = AsyncSession(self._engine, expire_on_commit=False)
            self.uow = UnitOfWork(self._session)
        return self.uow
