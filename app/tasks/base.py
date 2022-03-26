from celery import Task
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitch_repository import TwitchRepository
from app.db.uow import UnitOfWork
from app.api.dependencies.get_db import engine


class DatabaseTask(Task):
    _kraken_repository = None
    _twitch_repository = None
    _auto_tasks_repository = None

    @property
    def kraken_repository(self):
        if self._kraken_repository is None:
            session = AsyncSession(engine, expire_on_commit=False)
            uow = UnitOfWork(session)
            self._kraken_repository = KrakenRepository(uow)
        return self._kraken_repository

    @property
    def twitch_repository(self):
        if self._twitch_repository is None:
            session = AsyncSession(engine, expire_on_commit=False)
            uow = UnitOfWork(session)
            self._twitch_repository = TwitchRepository(uow)
        return self._twitch_repository

    @property
    def auto_tasks_repository(self):
        if self._auto_tasks_repository is None:
            session = AsyncSession(engine, expire_on_commit=False)
            uow = UnitOfWork(session)
            self._auto_tasks_repository = AutoTasksRepository(uow)
        return self._auto_tasks_repository
