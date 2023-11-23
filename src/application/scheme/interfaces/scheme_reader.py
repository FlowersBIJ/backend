from abc import ABC, abstractmethod
from uuid import UUID

from src.application.common.filters.filter import Filters
from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.schemes import Schemes


class SchemeReader(ABC):
    @abstractmethod
    async def get_by_id(self, scheme_id: UUID) -> Scheme:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Scheme:
        raise NotImplementedError

    @abstractmethod
    async def get_schemes(self, filters: Filters) -> Schemes:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, deleted: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_id(self, scheme_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, name: str) -> bool:
        raise NotImplementedError
