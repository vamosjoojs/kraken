from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TwitchClips, Kraken


class TwitchRepository(BaseRepository[TwitchClips]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitchClips)

    async def update_status(self, twitch_model: TwitchClips) -> int:
        qb = sa.select(TwitchClips).where(TwitchClips.id == twitch_model.id)
        result = await self.uow.session.execute(qb)
        data = result.scalars().first()

        async with self.uow as uow:
            data.post_status = twitch_model.post_status
            await uow.session.commit()

        return twitch_model.id

    async def get_twitch_clips_by_clip_url(self, clip_url: str) -> TwitchClips:
        qb = sa.select(TwitchClips).where(TwitchClips.clip_url == clip_url)
        result = await self.uow.session.execute(qb)
        return result.scalars().first()

    async def get_twitch_clips_by_clip_id(self, clip_id: str) -> TwitchClips:
        qb = sa.select(TwitchClips)\
            .options(joinedload(TwitchClips.kraken))\
            .where(TwitchClips.clip_id == clip_id)

        result = await self.uow.session.execute(qb)
        return result.scalars().first()
