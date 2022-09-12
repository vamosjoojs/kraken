import math
from typing import List

import sqlalchemy as sa
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Query

from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import KrakenClips, Kraken
from app.models.schemas.common.paginated import Paginated


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

    def get_clips_by_kraken_head(self, page: int, page_size: int, kraken_head: str):
        kraken_clips_sq = (sa.select(KrakenClips).distinct(KrakenClips.clip_name).where(KrakenClips.kraken_head == kraken_head).order_by(KrakenClips.clip_name).subquery())
        qb = sa.select(KrakenClips).join(kraken_clips_sq, KrakenClips.id == kraken_clips_sq.c.id).order_by(desc(kraken_clips_sq.c.created_at))

        return self.paginate_query(qb, page, page_size)


