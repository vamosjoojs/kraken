import enum
from typing import Optional
from pydantic import BaseModel


class OrderPage(enum.Enum):
    asc = "asc"
    desc = "desc"


class Sort(BaseModel):
    order_by: Optional[str] = None
    order: OrderPage
