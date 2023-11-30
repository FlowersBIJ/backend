from abc import ABC, abstractmethod

from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_type_create import BoxTypeCreate
from src.application.enums.box_type.dto.box_type_update import BoxTypeUpdate


class BoxTypeMutator(ABC):
    @abstractmethod
    async def add(self, box: BoxTypeCreate) -> BoxType:
        raise NotImplementedError
    
    @abstractmethod
    async def change_visibility(self, box: BoxTypeUpdate) -> BoxType:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, box: BoxTypeUpdate) -> BoxType:
        raise NotImplementedError
    