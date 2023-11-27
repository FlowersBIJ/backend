from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.client.dto.client import Client
from src.application.client.dto.clients import Clients


class ClientReader(ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def get_clients(self, filters: Filters) -> Clients:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self, invisible: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_name(self, name: str) -> bool:
        raise NotImplementedError