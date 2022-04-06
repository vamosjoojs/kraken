from typing import List

import sqlalchemy as sa

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TwitterSendMessage


class TwitterSendMessageRepository(BaseRepository[TwitterSendMessage]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitterSendMessage)

    def get_users_by_twitter_handle(self, twitter_handle: str) -> List[TwitterSendMessage]:
        qb = sa.select(TwitterSendMessage).where(TwitterSendMessage.twitter_handle == twitter_handle)
        result = self.uow.session.execute(qb)
        return result.scalars().all()
