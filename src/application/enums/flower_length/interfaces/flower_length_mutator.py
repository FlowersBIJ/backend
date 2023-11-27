from abc import ABC, abstractmethod

from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flower_length_create import FlowerLengthCreate
from src.application.enums.flower_length.dto.flower_length_update import FlowerLengthUpdate


class FlowerLengthMutator(ABC):
    @abstractmethod
    async def add(self, flower: FlowerLengthCreate) -> FlowerLength:
        raise NotImplementedError
    
    @abstractmethod
    async def change_visibility(self, flower_length: FlowerLengthUpdate) -> FlowerLength:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, flower_length: FlowerLengthUpdate) -> FlowerLength:
        raise NotImplementedError
    