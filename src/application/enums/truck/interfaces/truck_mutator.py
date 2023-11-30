from abc import ABC, abstractmethod

from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.truck_create import TruckCreate
from src.application.enums.truck.dto.truck_update import TruckUpdate


class TruckMutator(ABC):
    @abstractmethod
    async def add(self, truck: TruckCreate) -> Truck:
        raise NotImplementedError
    
    @abstractmethod
    async def change_visibility(self, truck: TruckUpdate) -> Truck:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, truck: TruckUpdate) -> Truck:
        raise NotImplementedError
    