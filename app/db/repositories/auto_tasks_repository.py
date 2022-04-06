import datetime

import sqlalchemy as sa
from sqlalchemy import and_

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import AutoTasks


class AutoTasksRepository(BaseRepository[AutoTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, AutoTasks)

    def get_instagram_state_switch(self, id) -> AutoTasks:
        qb = sa.select(AutoTasks).where(AutoTasks.id == id)

        qb = qb.where(and_(
                AutoTasks.activated_at <= datetime.datetime.utcnow(),
                AutoTasks.deactivated_at >= datetime.datetime.utcnow()))

        result = self.uow.session.execute(qb)
        return result.scalars().first()

    async def disable_task(self, id: int) -> int:
        qb = sa.select(AutoTasks).where(AutoTasks.id == id)
        result = await self.uow.session.execute(qb)
        data = result.scalars().first()

        async with self.uow as uow:
            data.deactivated_at = datetime.datetime.utcnow()
            await uow.session.commit()

        return id
