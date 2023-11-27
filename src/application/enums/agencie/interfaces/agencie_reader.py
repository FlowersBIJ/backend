from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencies import Agencies


class AgencieReader(ABC):
    @abstractmethod
    async def get_by_name(self, agencie_name: str) -> Agencie:
        raise NotImplementedError

    @abstractmethod
    async def get_agencies(self, filters: Filters) -> Agencies:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, agencie_name: str) -> bool:
        raise NotImplementedError
    