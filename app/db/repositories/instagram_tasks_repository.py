from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities.instagram_tasks import InstagramTasks
import sqlalchemy as sa
from typing import List


class InstagramTasksRepository(BaseRepository[InstagramTasks]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, InstagramTasks)

    def get_tasks(self) -> List[InstagramTasks]:
        qb = sa.select(InstagramTasks).where(InstagramTasks.activated.is_(True))
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def get_task_by_id(self, id: int):
        qb = sa.select(InstagramTasks).where(InstagramTasks.id == id)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_task_by_instagram_handle(self, instagram_handle: str) -> InstagramTasks:
        qb = sa.select(InstagramTasks).where(InstagramTasks.twitter_handle == instagram_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().first()
    #
    # def update_message_task(self, id: int, edit_message_task: TwitterTasks) -> int:
    #     qb = sa.select(TwitterTasks).where(TwitterTasks.id == id)
    #     result = self.uow.session.execute(qb)
    #     data = result.scalars().first()
    #
    #     with self.uow as uow:
    #         data.oauth_token = edit_message_task.oauth_token
    #         data.oauth_secret = edit_message_task.oauth_secret
    #         data.consumer_key = edit_message_task.consumer_key
    #         data.consumer_secret = edit_message_task.consumer_secret
    #         data.twitter_messages.tag = edit_message_task.twitter_messages.tag
    #         data.twitter_messages.message = edit_message_task.twitter_messages.message
    #         data.twitter_handle = edit_message_task.twitter_handle
    #         data.twitter_messages.result_type = edit_message_task.twitter_messages.result_type
    #         data.activated = edit_message_task.activated
    #         uow.session.commit()
    #
    #     return id
    #
    # def add_follow(self, twitter_handle: str, twitter_follow: TwitterFollow):
    #     qb = sa.select(TwitterTasks).where(TwitterTasks.twitter_handle == twitter_handle)
    #     result = self.uow.session.execute(qb)
    #     data = result.scalars().first()
    #
    #     with self.uow as uow:
    #         data.twitter_follow = twitter_follow
    #         uow.session.commit()
    #
    #     return data.id

    def update_follow_task(self, id, orm_model):
        pass
