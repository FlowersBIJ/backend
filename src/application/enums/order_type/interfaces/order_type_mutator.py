from abc import ABC, abstractmethod

from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_type_create import OrderTypeCreate
from src.application.enums.order_type.dto.order_type_update import OrderTypeUpdate


class OrderTypeMutator(ABC):
    @abstractmethod
    async def add(self, order: OrderTypeCreate) -> OrderType:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, order: OrderTypeUpdate) -> OrderType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, order: OrderTypeUpdate) -> None:
        raise NotImplementedError
