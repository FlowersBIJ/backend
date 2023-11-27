from src.application.common.dto import DataTransferObject
from src.application.order.dto.order import Order
from src.application.order.dto.order_create import OrderCreate
from src.application.order.dto.order_update import OrderUpdate


OrderDTO = Order | OrderCreate | OrderUpdate


class Orders(DataTransferObject):
    orders: list[OrderDTO]
    total: int
    offset: int | None = None
    limit: int | None = None