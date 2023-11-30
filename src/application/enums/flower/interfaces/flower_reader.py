from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flowers import Flowers


class FlowerReader(ABC):
    @abstractmethod
    async def get_by_name(self, flower_name: str) -> Flower:
        raise NotImplementedError

    @abstractmethod
    async def get_flowers(self, filters: Filters) -> Flowers:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, flower_name: str) -> bool:
        raise NotImplementedError
    