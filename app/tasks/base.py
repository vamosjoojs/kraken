from celery import Task

from app.db.uow import UnitOfWork
from app.api.dependencies.get_db import engine, SessionLocal


class DatabaseTask(Task):
    _session = None
    _engine = engine

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()
            self._engine.dispose()

    @property
    def get_db(self):
        if self._session is None:
            self._session = SessionLocal()
            self.uow = UnitOfWork(self._session)
        return self.uow
