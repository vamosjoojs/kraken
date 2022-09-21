from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TwitterFollow
from app.models.entities.reddit_tasks import RedditTasks
import sqlalchemy as sa
from typing import List


class RedditTasksRepository(BaseRepository[RedditTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, RedditTasks)

    def get_tasks(self) -> List[RedditTasks]:
        qb = sa.select(RedditTasks)
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def get_task_by_id(self, id: int):
        qb = sa.select(RedditTasks).where(RedditTasks.id == id)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_task_by_reddit_handle(self, reddit_handle: str) -> RedditTasks:
        qb = sa.select(RedditTasks).where(RedditTasks.reddit_handle == reddit_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def update_message_task(self, id: int, edit_message_task: RedditTasks) -> int:
        qb = sa.select(RedditTasks).where(RedditTasks.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.client_id = edit_message_task.client_id
            data.client_secret = edit_message_task.client_secret
            data.username = edit_message_task.username
            data.password = edit_message_task.password
            data.reddit_messages.tag = edit_message_task.reddit_messages.tag
            data.reddit_messages.message = edit_message_task.reddit_messages.message
            data.reddit_handle = edit_message_task.reddit_handle
            data.activated = edit_message_task.activated
            uow.session.commit()

        return id
