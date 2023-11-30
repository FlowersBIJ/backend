from abc import ABC, abstractmethod

from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencie_create import AgencieCreate
from src.application.enums.agencie.dto.agencie_update import AgencieUpdate


class AgencieMutator(ABC):
    @abstractmethod
    async def add(self, flower: AgencieCreate) -> Agencie:
        raise NotImplementedError
    
    @abstractmethod
    async def change_visibility(self, flower: AgencieUpdate) -> Agencie:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, flower: AgencieUpdate) -> Agencie:
        raise NotImplementedError
    