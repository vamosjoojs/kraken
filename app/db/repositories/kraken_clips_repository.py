from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import KrakenClips


class KrakenClipsRepository(BaseRepository[KrakenClips]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, KrakenClips)

    def get_clips_by_clip_url(self, clip_url: str) -> KrakenClips:
        qb = sa.select(KrakenClips).where(KrakenClips.clip_url == clip_url)
        result = self.uow.session.execute(qb)
        return result.scalars().first()

    def get_clips_by_clip_id(self, clip_id: str) -> List[KrakenClips]:
        qb = sa.select(KrakenClips)\
            .options(joinedload(KrakenClips.kraken))\
            .where(KrakenClips.clip_id == clip_id)

        result = self.uow.session.execute(qb)
        return result.scalars().unique().all()

    def get_clips_by_id(self, id: int) -> KrakenClips:
        qb = sa.select(KrakenClips) \
            .options(joinedload(KrakenClips.kraken)) \
            .where(KrakenClips.id == id)

        result = self.uow.session.execute(qb)
        return result.scalars().unique().first()

    def get_clips(self, clip_id: str) -> List[KrakenClips]:
        qb = sa.select(KrakenClips).options(joinedload(KrakenClips.kraken)) \
            .where(KrakenClips.clip_id == clip_id)

        result = self.uow.session.execute(qb)
        return result.scalars().unique().all()