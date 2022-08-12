from typing import List

import sqlalchemy as sa
from app.db.uow import UnitOfWork
from app.db.repositories.base_repository import BaseRepository
from app.models.entities import Parameters


class ParametersRepository(BaseRepository[Parameters]):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow, Parameters)

    def get_parameters(self) -> List[Parameters]:
        qb = sa.select(Parameters)
        result = self.uow.session.execute(qb)
        return result.scalars().all()

    def update_parameter(self, id: int, orm_model: Parameters):
        qb = sa.select(Parameters).where(Parameters.id == id)
        result = self.uow.session.execute(qb)
        data = result.scalars().first()

        with self.uow as uow:
            data.name = orm_model.name
            data.activated = orm_model.activated
            data.value = orm_model.value
            data.bool_value = orm_model.bool_value
            data.int_value = orm_model.int_value
            uow.session.commit()

        return id
