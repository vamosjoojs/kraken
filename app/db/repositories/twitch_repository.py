from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import TwitchClips


class TwitchRepository(BaseRepository[TwitchClips]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, TwitchClips)

    def get_twitch_clips_by_clip_url(self, clip_url: str) -> TwitchClips:
        qb = sa.select(TwitchClips).where(TwitchClips.clip_url == clip_url)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_twitch_clips_by_clip_id(self, clip_id: str) -> List[TwitchClips]:
        qb = sa.select(TwitchClips)\
            .options(joinedload(TwitchClips.kraken))\
            .where(TwitchClips.clip_id == clip_id)

        result = self.uow.session.execute(qb)
        return result.scalars().unique().all()
