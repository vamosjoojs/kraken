from typing import List
from sqlalchemy.orm import joinedload

import sqlalchemy as sa
from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import Kraken


class KrakenRepository(BaseRepository[Kraken]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, Kraken)

    async def update_status(self, kraken_model: Kraken) -> int:
        qb = sa.select(Kraken).where(Kraken.id == kraken_model.id)
        result = await self.uow.session.execute(qb)
        data = result.scalars().first()

        async with self.uow as uow:
            data.post_status = kraken_model.post_status
            await uow.session.commit()

        return kraken_model.id

    async def get_queue_posts(self) -> List[Kraken]:
        qb = sa.select(Kraken).options(joinedload(Kraken.twitch_clips))

        result = await self.uow.session.execute(qb)
        return result.scalars().all()
