import uuid
from abc import ABC, abstractmethod

from src.application.box.dto.box import Box
from src.application.box.dto.box_create import BoxCreate
from src.application.box.dto.box_update import BoxUpdate


class BoxMutator(ABC):
    @abstractmethod
    async def add(self, box: BoxCreate) -> Box:
        raise NotImplementedError

    @abstractmethod
    async def update(self, box_id: uuid.UUID, box: BoxUpdate) -> Box:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, box_id: uuid.UUID) -> Box:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, box_id: uuid.UUID) -> Box:
        raise NotImplementedError