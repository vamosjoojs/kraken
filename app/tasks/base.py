from celery import Task
from sqlalchemy.ext.asyncio.session import AsyncSession
import asyncio

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitch_repository import TwitchRepository
from app.db.repositories.twitter_repository import TwitterSendMessageRepository
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
    def kraken_repository(self):
        if self._session is None:
            self._session = AsyncSession(self._engine, expire_on_commit=False)
            uow = UnitOfWork(self._session)
            self._kraken_repository = KrakenRepository(uow)
        return self._kraken_repository

    @property
    def twitch_repository(self):
        if self._session is None:
            self._session = AsyncSession(self._engine, expire_on_commit=False)
            uow = UnitOfWork(self._session)
            self._twitch_repository = TwitchRepository(uow)
        return self._twitch_repository

    @property
    def auto_tasks_repository(self):
        if self._session is None:
            self._session = AsyncSession(self._engine, expire_on_commit=False)
            uow = UnitOfWork(self._session)
            self._auto_tasks_repository = AutoTasksRepository(uow)
        return self._auto_tasks_repository

    @property
    def twitter_repository(self):
        if self._session is None:
            self._session = AsyncSession(self._engine, expire_on_commit=False)
            uow = UnitOfWork(self._session)
            self._twitter_repository = TwitterSendMessageRepository(uow)
        return self._twitter_repository
