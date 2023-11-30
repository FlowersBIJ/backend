from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.trucks import Trucks


class TruckReader(ABC):
    @abstractmethod
    async def get_by_name(self, truck_name: str) -> Truck:
        raise NotImplementedError

    @abstractmethod
    async def get_trucks(self, filters: Filters) -> Trucks:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, truck_name: str) -> bool:
        raise NotImplementedError
    