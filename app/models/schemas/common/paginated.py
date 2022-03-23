from typing import Generic, List, TypeVar
from pydantic.generics import GenericModel

SchemaType = TypeVar("SchemaType")


class Paginated(GenericModel, Generic[SchemaType]):
    total_items: int
    total_pages: int
    current_page: int
    items: List[SchemaType]
