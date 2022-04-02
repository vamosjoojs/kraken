from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities.twitter_tasks import TwitterTasks
import sqlalchemy as sa
from typing import List


class TwitterTasksRepository(BaseRepository[TwitterTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitterTasks)

    async def get_tasks(self) -> List[TwitterTasks]:
        qb = sa.select(TwitterTasks).where(TwitterTasks.activated == True)
        result = await self.uow.session.execute(qb)
        return result.scalars().all()
