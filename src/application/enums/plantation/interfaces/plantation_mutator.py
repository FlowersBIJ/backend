from abc import ABC, abstractmethod

from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantation_create import PlantationCreate
from src.application.enums.plantation.dto.plantation_update import PlantationUpdate


class PlantationMutator(ABC):
    @abstractmethod
    async def add(self, plantation: PlantationCreate) -> Plantation:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, plantation: PlantationUpdate) -> Plantation:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, plantation: PlantationUpdate) -> None:
        raise NotImplementedError
