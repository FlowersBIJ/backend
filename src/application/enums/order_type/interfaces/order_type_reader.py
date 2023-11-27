from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_types import OrderTypes


class OrderTypeReader(ABC):
    @abstractmethod
    async def get_by_name(self, typename: str) -> OrderType:
        raise NotImplementedError

    @abstractmethod
    async def get_types(self, filters: Filters) -> OrderTypes:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, typename: str) -> bool:
        raise NotImplementedError
    