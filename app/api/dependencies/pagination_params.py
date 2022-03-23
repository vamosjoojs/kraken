from app.models.schemas.common.sort import Sort, OrderPage


class PaginationParams:
    def __init__(
        self,
        page: int = 1,
        page_size: int = 15,
        order_by: str = None,
        order: OrderPage = OrderPage.asc,
    ):
        self.page = page
        self.page_size = page_size
        self.sort = Sort(order_by=order_by, order=order)
