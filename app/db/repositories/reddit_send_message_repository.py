from typing import List

import sqlalchemy as sa

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities.reddit_send_message import RedditSendMessage


class RedditSendMessageRepository(BaseRepository[RedditSendMessage]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, RedditSendMessage)

    def get_users_by_reddit_handle(self, reddit_handle: str, status: bool = True) -> List[RedditSendMessage]:
        qb = sa.select(RedditSendMessage).where(RedditSendMessage.reddit_handle == reddit_handle and RedditSendMessage.sended == status)
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def update_sended(self, id: int, status: bool):
        qb = sa.select(RedditSendMessage).where(RedditSendMessage.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.sended = status
            uow.session.commit()

