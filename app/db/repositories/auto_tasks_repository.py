import datetime

import sqlalchemy as sa
from sqlalchemy import and_

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import AutoTasks


class AutoTasksRepository(BaseRepository[AutoTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, AutoTasks)

    async def get_instagram_state_switch(self, id):
        qb = sa.select(AutoTasks).where(AutoTasks.id == id)

        qb = qb.where(and_(
                AutoTasks.activated_at <= datetime.datetime.utcnow(),
                AutoTasks.deactivated_at >= datetime.datetime.utcnow()))

        result = await self.uow.session.execute(qb)
        return result.scalars().first()
