from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities.twitter_messages import TwitterMessages
import sqlalchemy as sa
from typing import List


class TwitterMessagesRepository(BaseRepository[TwitterMessages]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitterMessages)

    def get_tasks(self) -> List[TwitterMessages]:
        qb = sa.select(TwitterMessages).where(TwitterMessages.twitter_tasks.activated.is_(True))
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def get_task_by_id(self, id: int):
        qb = sa.select(TwitterMessages).where(TwitterMessages.twitter_tasks.id == id)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_task_by_twitter_handle(self, twitter_handle: str) -> TwitterMessages:
        qb = sa.select(TwitterMessages).where(TwitterMessages.twitter_handle == twitter_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def update_task(self, id: int, edit_message_task: TwitterMessages) -> int:
        qb = sa.select(TwitterMessages).where(TwitterMessages.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.tag = edit_message_task.tag
            data.message = edit_message_task.message
            data.twitter_handle = edit_message_task.twitter_handle
            data.result_type = edit_message_task.result_type
            data.twitter_tasks.activated = edit_message_task.twitter_tasks.activated
            uow.session.commit()

        return id
