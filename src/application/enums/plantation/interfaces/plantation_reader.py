from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantations import Plantations


class PlantationReader(ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Plantation:
        raise NotImplementedError

    @abstractmethod
    async def get_plantations(self, filters: Filters) -> Plantations:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, name: str) -> bool:
        raise NotImplementedError
    