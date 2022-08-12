from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TwitterFollow
from app.models.entities.twitter_tasks import TwitterTasks
import sqlalchemy as sa
from typing import List


class TwitterTasksRepository(BaseRepository[TwitterTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitterTasks)

    def get_tasks(self) -> List[TwitterTasks]:
        qb = sa.select(TwitterTasks)
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def get_task_by_id(self, id: int):
        qb = sa.select(TwitterTasks).where(TwitterTasks.id == id)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_task_by_twitter_handle(self, twitter_handle: str) -> TwitterTasks:
        qb = sa.select(TwitterTasks).where(TwitterTasks.twitter_handle == twitter_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def update_message_task(self, id: int, edit_message_task: TwitterTasks) -> int:
        qb = sa.select(TwitterTasks).where(TwitterTasks.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.oauth_token = edit_message_task.oauth_token
            data.oauth_secret = edit_message_task.oauth_secret
            data.consumer_key = edit_message_task.consumer_key
            data.consumer_secret = edit_message_task.consumer_secret
            data.twitter_messages.tag = edit_message_task.twitter_messages.tag
            data.twitter_messages.message = edit_message_task.twitter_messages.message
            data.twitter_handle = edit_message_task.twitter_handle
            data.twitter_messages.result_type = edit_message_task.twitter_messages.result_type
            data.activated = edit_message_task.activated
            data.is_trending_user = edit_message_task.is_trending_user
            uow.session.commit()

        return id

    def add_follow(self, twitter_handle: str, twitter_follow: TwitterFollow):
        qb = sa.select(TwitterTasks).where(TwitterTasks.twitter_handle == twitter_handle)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.twitter_follow = twitter_follow
            uow.session.commit()

        return data.id
