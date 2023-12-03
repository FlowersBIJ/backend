from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flowers_length import FlowersLength


class FlowerLengthReader(ABC):
    @abstractmethod
    async def get_by_flower_name_and_sort(
        self, flower_name: str, flower_sort: str, filters: Filters
    ) -> FlowersLength:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, filters: Filters) -> FlowersLength:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_sort(self, flower_length: FlowerLength) -> bool:
        raise NotImplementedError
