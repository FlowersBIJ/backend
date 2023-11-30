from abc import ABC, abstractmethod

from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flower_sort_create import FlowerSortCreate
from src.application.enums.flower_sort.dto.flower_sort_update import FlowerSortUpdate


class FlowerSortMutator(ABC):
    @abstractmethod
    async def add(self, flower: FlowerSortCreate) -> FlowerSort:
        raise NotImplementedError
    
    @abstractmethod
    async def change_visibility(self, flower_sort: FlowerSortUpdate) -> FlowerSort:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, flower_sort: FlowerSortUpdate) -> FlowerSort:
        raise NotImplementedError
    