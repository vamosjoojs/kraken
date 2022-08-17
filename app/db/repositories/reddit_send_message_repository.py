from typing import List

import sqlalchemy as sa

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities.reddit_send_message import RedditSendMessage


class RedditSendMessageRepository(BaseRepository[RedditSendMessage]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, RedditSendMessage)

    def get_users_by_reddit_handle(self, reddit_handle: str) -> List[RedditSendMessage]:
        qb = sa.select(RedditSendMessage).where(RedditSendMessage.reddit_handle == reddit_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().all()
