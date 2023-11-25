from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flowers_sorts import FlowersSorts


class FlowerSortReader(ABC):
    @abstractmethod
    async def get_by_flower_name(self, name: str, filters: Filters) -> FlowersSorts:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, filters: Filters) -> FlowersSorts:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def check_exists_by_sort(self, sort: FlowerSort) -> bool:
        raise NotImplementedError
    