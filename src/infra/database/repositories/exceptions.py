from dataclasses import dataclass
from typing import TypeVar, Generic

from src.application.common.dto import DTOCreate, DTOUpdate
from src.application.common.exceptions import ApplicationException


EntityCreateType = TypeVar("EntityCreateType", bound=DTOCreate)
EntityUpdateType = TypeVar("EntityUpdateType", bound=DTOUpdate)


@dataclass(eq=False)
class EntityNotFoundException(ApplicationException):
    entity_id: str
    entity_type: str

    @property
    def message(self) -> str:
        return f"{self.entity_type} not found with id: {self.entity_id}"


@dataclass(eq=False)
class EntityCreateException(ApplicationException, Generic[EntityCreateType]):
    entity: EntityCreateType

    @property
    def message(self) -> str:
        return (
            f"Can't create {self.entity.__class__.__name__} by payload: {self.entity}"
        )


@dataclass(eq=False)
class EntityUpdateException(ApplicationException, Generic[EntityUpdateType]):
    entity: EntityUpdateType

    @property
    def message(self) -> str:
        return (
            f"Can't update {self.entity.__class__.__name__} by payload: {self.entity}"
        )


@dataclass(eq=False)
class EntityDeleteException(ApplicationException):
    entity_id: str
    entity_type: str

    @property
    def message(self) -> str:
        return f"Can't delete {self.entity_type} by id: {self.entity_id}"
