from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_types import BoxTypes


class BoxTypeReader(ABC):
    @abstractmethod
    async def get_by_name(self, typename: str) -> BoxType:
        raise NotImplementedError

    @abstractmethod
    async def get_types(self, filters: Filters) -> BoxTypes:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, typename: str) -> bool:
        raise NotImplementedError
    