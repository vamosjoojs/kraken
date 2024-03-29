from datetime import datetime, date
from typing import List
from sqlalchemy.sql import func
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

import sqlalchemy as sa
from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import Kraken, KrakenClips


class KrakenRepository(BaseRepository[Kraken]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, Kraken)

    def update_status(self, kraken_model: Kraken) -> int:
        qb = sa.select(Kraken).where(Kraken.id == kraken_model.id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.post_status = kraken_model.post_status
            uow.session.commit()

        return kraken_model.id

    def get_queue_posts(self, page: int, page_size: int):
        latest_kraken_subq = sa.select(
            Kraken.kraken_hand,
            func.max(Kraken.created_at).label('latest_created_at')
        ).group_by(
            Kraken.kraken_hand
        ).subquery()

        latest_kraken_query = sa.select(
            Kraken, KrakenClips
        ).join(
            KrakenClips, Kraken.kraken_clips_id == KrakenClips.id
        ).join(
            latest_kraken_subq,
            (Kraken.kraken_hand == latest_kraken_subq.c.kraken_hand) &
            (Kraken.created_at == latest_kraken_subq.c.latest_created_at)
        )

        return self.paginate_query(latest_kraken_query, page, page_size)

    def get_by_clip_id(self, clip_id: str):
        qb = sa.select(Kraken).where(Kraken.kraken_clips_id == clip_id)

        result = self.uow.session.execute(qb)
        return result.scalars().unique().all()

    def get_queue_post_by_date(self, initial_date: date, finish_date: date, post_status: str) -> List[Kraken]:
        qb = sa.select(Kraken).options(joinedload(Kraken.kraken_clips)).order_by(desc(Kraken.schedule), desc(Kraken.id))
        qb = qb.where(Kraken.schedule != None)
        qb = qb.where(Kraken.schedule >= initial_date)
        qb = qb.where(Kraken.schedule <= finish_date)
        qb = qb.where(Kraken.post_status == post_status)

        result = self.uow.session.execute(qb)
        data = result.scalars().all()
        return data
