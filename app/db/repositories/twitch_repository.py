from typing import List

import sqlalchemy as sa
from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import Twitch


class TwitchRepository(BaseRepository[Twitch]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, Twitch)

    async def insert_or_update(self, twitch_model: Twitch) -> int:
        qb = sa.select(Twitch).where(Twitch.clip_url == twitch_model.clip_url)
        result = await self.uow.session.execute(qb)
        data = result.scalars().first()

        async with self.uow as uow:
            if data:
                data.post_status = twitch_model.post_status
                await uow.session.commit()
            else:
                uow.session.add(twitch_model)

        return twitch_model.id

    async def get_twitch_clips_by_clip_url(self, clip_url: str) -> Twitch:
        qb = sa.select(Twitch).where(Twitch.clip_url == clip_url)
        result = await self.uow.session.execute(qb)
        return result.scalars().first()

    async def get_queue_twitch_posts(self) -> List[Twitch]:
        qb = sa.select(Twitch)
        result = await self.uow.session.execute(qb)
        return result.scalars().all()
