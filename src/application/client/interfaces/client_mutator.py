from abc import ABC, abstractmethod

from src.application.client.dto.client import Client
from src.application.client.dto.client_create import ClientCreate
from src.application.client.dto.client_update import ClientUpdate


class ClientMutator(ABC):
    @abstractmethod
    async def add(self, client: ClientCreate) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def update(self, client_name: str, client: ClientUpdate) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, client_name: str) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, client_name: str) -> Client:
        raise NotImplementedError