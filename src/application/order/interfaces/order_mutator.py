import uuid
from abc import ABC, abstractmethod

from src.application.order.dto.order import Order
from src.application.order.dto.order_create import OrderCreate
from src.application.order.dto.order_update import OrderUpdate


class OrderMutator(ABC):
    @abstractmethod
    async def add(self, order: OrderCreate) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def update(self, order_id: uuid.UUID, order: OrderUpdate) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, order_id: uuid.UUID) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, order_id: uuid.UUID) -> Order:
        raise NotImplementedError