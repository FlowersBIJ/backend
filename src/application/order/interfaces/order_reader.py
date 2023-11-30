import uuid
from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.order.dto.order import Order
from src.application.order.dto.orders import Orders


class OrderReader(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: uuid.UUID) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def get_orders(self, filters: Filters) -> Orders:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, visible: bool | None = None) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_id(self, order_id: uuid.UUID) -> bool:
        raise NotImplementedError
