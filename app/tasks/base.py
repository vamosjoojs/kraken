from celery import Task
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.db.repositories.twitch_repository import TwitchRepository
from app.db.uow import UnitOfWork
from app.api.dependencies.get_db import engine


class DatabaseTask(Task):
    _twitch_repository = None

    @property
    def twitch_repository(self):
        if self._twitch_repository is None:
            session = AsyncSession(engine, expire_on_commit=False)
            uow = UnitOfWork(session)
            self._twitch_repository = TwitchRepository(uow)
        return self._twitch_repository

