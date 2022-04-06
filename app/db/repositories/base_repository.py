from app.models.entities import BaseModel
from app.models.schemas.common.sort import OrderPage, Sort
import math
import sqlalchemy as sa
from sqlalchemy.orm import Query
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union, Generic
from app.db.uow import UnitOfWork
from app.models.schemas.common.paginated import Paginated
from sqlalchemy import asc, desc


MappingType = TypeVar("MappingType", bound=BaseModel)


class BaseRepository(Generic[MappingType]):
    def __init__(self, uow: UnitOfWork, mapping: Type[MappingType]):
        self.uow = uow
        self.mapping = mapping

    def add(self, batch):
        with self.uow as uow:
            uow.session.add(batch)
            uow.session.flush()
        return batch

    @staticmethod
    def sort_query(
        query: Union[Query, sa.sql.Select],
        sort: Sort,
        sort_map: Optional[Dict[str, Callable[[Query, Any], Query]]] = None,
    ) -> Query:
        if sort is not None and sort.order_by is not None:
            sort_function = desc if sort.order == OrderPage.desc else asc
            if sort_map is not None and sort.order_by in sort_map.keys():
                query = sort_map[sort.order_by](query, sort_function)
                return query
            sort_query = sort_function(sort.order_by)
            query = query.order_by(sort_query)
        return query

    def _paginate(self, select: Query, page: int, page_size: int):
        qb_count = sa.select(sa.func.count()).select_from(select.order_by(None))
        query_result = self.uow.session.execute(qb_count)
        total = query_result.scalars().first()
        paginated_qb = select.offset((page - 1) * page_size).limit(page_size)
        pages = int(math.ceil(total / float(page_size)))
        result = self.uow.session.execute(paginated_qb)
        return result, total, pages

    def paginate_query(
        self, select: Query, model: Type[MappingType], page: int, page_size: int
    ):
        result, total, pages = self._paginate(select, page, page_size)
        registers = result.unique().scalars().all()
        items = list(map(model.from_orm, registers))
        return Paginated(
            total_items=total, current_page=page, total_pages=pages, items=items
        )
