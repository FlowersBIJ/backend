import uuid
from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.flower_in_box.dto.flower_in_box import FlowerInBox
from src.application.flower_in_box.dto.flowers_in_box import FlowersInBox


class FlowerInBoxReader(ABC):
    @abstractmethod
    async def get_by_id(self, flower_id: uuid.UUID) -> FlowerInBox:
        raise NotImplementedError

    @abstractmethod
    async def get_flowers(self, filters: Filters) -> FlowersInBox:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_id(self, flower_id: uuid.UUID) -> bool:
        raise NotImplementedError