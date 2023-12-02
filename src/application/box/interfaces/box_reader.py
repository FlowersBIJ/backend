import uuid
from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.box.dto.box import Box
from src.application.box.dto.boxes import Boxes


class BoxReader(ABC):
    @abstractmethod
    async def get_by_id(self, box_id: uuid.UUID) -> Box:
        raise NotImplementedError

    @abstractmethod
    async def get_boxes(self, filters: Filters) -> Boxes:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, visible: bool = True) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_id(self, box_id: uuid.UUID) -> bool:
        raise NotImplementedError
