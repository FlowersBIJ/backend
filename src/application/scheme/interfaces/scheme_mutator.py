from abc import ABC, abstractmethod
from uuid import UUID

from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.scheme_create import SchemeCreate
from src.application.scheme.dto.scheme_update import SchemeUpdate


class SchemeMutator(ABC):
    @abstractmethod
    async def add(self, scheme: SchemeCreate) -> Scheme:
        raise NotImplementedError

    @abstractmethod
    async def update(self, scheme_id: UUID, order: SchemeUpdate) -> Scheme:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, scheme_id: UUID) -> Scheme:
        raise NotImplementedError
