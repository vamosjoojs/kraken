from app.models.schemas.common.sort import OrderPage, Sort
import math
import sqlalchemy as sa
from sqlalchemy.orm import Query
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union, Generic
from app.db.uow import UnitOfWork
from app.models.schemas.base import Base
from app.models.schemas.common.paginated import Paginated
from sqlalchemy import asc, desc

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, uow: UnitOfWork, mapping: Type[ModelType]):
        self.uow = uow
        self.mapping = mapping

    async def add(self, batch):
        async with self.uow as uow:
            uow.session.add(batch)
            await uow.session.flush()
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

    async def _paginate(self, select: Query, page: int, page_size: int):
        qb_count = sa.select(sa.func.count()).select_from(select.order_by(None))
        query_result = await self.uow.session.execute(qb_count)
        total = query_result.scalars().first()
        paginated_qb = select.offset((page - 1) * page_size).limit(page_size)
        pages = int(math.ceil(total / float(page_size)))
        result = await self.uow.session.execute(paginated_qb)
        return result, total, pages

    async def paginate_query(
        self, select: Query, model: Type[ModelType], page: int, page_size: int
    ):
        result, total, pages = await self._paginate(select, page, page_size)
        registers = result.unique().scalars().all()
        items = list(map(model.from_orm, registers))
        return Paginated(
            total_items=total, current_page=page, total_pages=pages, items=items
        )
