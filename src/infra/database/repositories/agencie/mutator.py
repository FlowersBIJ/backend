from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencie_create import AgencieCreate
from src.application.enums.agencie.dto.agencie_update import AgencieUpdate
from src.application.enums.agencie.interfaces.agencie_mutator import AgencieMutator
from src.infra.database.models.client import Agencie as AgencieDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, AgencieMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, agencie: AgencieCreate) -> Agencie:
        new_agencie = AgencieDB()
        mutate_entity(new_agencie, agencie)

        try:
            self.db.add(new_agencie)
            await self.db.flush()
            await self.db.refresh(new_agencie)

            agencie_dto = Agencie.model_validate(new_agencie)
            return agencie_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(agencie)

    async def delete(self, agencie: AgencieUpdate) -> Agencie:
        agencie_db = await self.db.get(AgencieDB, agencie.agencie_name)

        if agencie_db is None:
            raise EntityNotFoundException(agencie.agencie_name, "Agencie")

        await self.db.delete(agencie_db)
        try:
            await self.db.flush()
            return None

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(agencie.agencie_name, "Agencie")

    async def change_visibility(self, agencie: AgencieUpdate) -> Agencie:
        agencie_db = await self.db.get(AgencieDB, agencie.agencie_name)

        if agencie_db is None:
            raise EntityNotFoundException(agencie.agencie_name, "Agencie")

        agencie_db.visible = not agencie_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(agencie_db)

            agencie_dto = Agencie.model_validate(agencie_db)
            return agencie_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(agencie.agencie_name, "Agencie")

    async def commit(self) -> None:
        await self.db.commit()
