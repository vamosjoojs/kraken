from typing import List
from sqlalchemy.orm import joinedload

import sqlalchemy as sa
from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import Kraken


class KrakenRepository(BaseRepository[Kraken]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, Kraken)

    async def get_queue_posts(self) -> List[Kraken]:
        qb = sa.select(Kraken).options(joinedload(Kraken.twitch_clips))

        result = await self.uow.session.execute(qb)
        return result.scalars().all()
