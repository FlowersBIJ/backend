import uuid
from abc import ABC, abstractmethod

from src.application.flower_in_box.dto.flower_in_box import FlowerInBox
from src.application.flower_in_box.dto.flower_in_box_create import FlowerInBoxCreate
from src.application.flower_in_box.dto.flower_in_box_update import FlowerInBoxUpdate


class FlowerInBoxMutator(ABC):
    @abstractmethod
    async def add(self, flower: FlowerInBoxCreate) -> FlowerInBox:
        raise NotImplementedError

    @abstractmethod
    async def update(self, flower_id: uuid.UUID, flower: FlowerInBoxUpdate) -> FlowerInBox:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, flower_id: uuid.UUID) -> FlowerInBox:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, flower_id: uuid.UUID) -> FlowerInBox:
        raise NotImplementedError