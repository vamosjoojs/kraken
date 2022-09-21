from datetime import datetime

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TiktokTasks
import sqlalchemy as sa
from typing import List


class TiktokTasksRepository(BaseRepository[TiktokTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TiktokTasks)

    def get_tasks(self) -> List[TiktokTasks]:
        qb = sa.select(TiktokTasks)
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def get_task_by_id(self, id: int):
        qb = sa.select(TiktokTasks).where(TiktokTasks.id == id)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_task_by_tiktok_handle(self, tiktok_handle: str) -> TiktokTasks:
        qb = sa.select(TiktokTasks).where(TiktokTasks.tiktok_handle == tiktok_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def update_message_task(self, id: int, access_token: str, expires_in: int, refresh_token: str) -> int:
        qb = sa.select(TiktokTasks).where(TiktokTasks.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.access_token = access_token
            data.expires_in = expires_in
            data.refresh_token = refresh_token
            data.updated_at = datetime.utcnow()
            uow.session.commit()

        return id
