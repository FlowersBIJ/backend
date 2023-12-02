from abc import ABC, abstractmethod

from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flower_create import FlowerCreate
from src.application.enums.flower.dto.flower_update import FlowerUpdate


class FlowerMutator(ABC):
    @abstractmethod
    async def add(self, flower: FlowerCreate) -> Flower:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, flower: FlowerUpdate) -> Flower:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, flower: FlowerUpdate) -> None:
        raise NotImplementedError
