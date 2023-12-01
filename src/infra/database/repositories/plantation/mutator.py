from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantation_create import PlantationCreate
from src.application.enums.plantation.dto.plantation_update import PlantationUpdate
from src.application.enums.plantation.interfaces.plantation_mutator import PlantationMutator
from src.infra.database.models.box import Plantation as PlantationDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, PlantationMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, plantation: PlantationCreate) -> Plantation:
        new_plantation = PlantationDB()
        mutate_entity(new_plantation, plantation)

        try:
            self.db.add(new_plantation)
            await self.db.flush()
            await self.db.refresh(new_plantation)

            plantation_dto = Plantation.model_validate(new_plantation)
            return plantation_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(plantation)

    async def delete(self, plantation: PlantationUpdate) -> Plantation:
        plantation_db = await self.db.get(PlantationDB, plantation.plantation_name)

        if plantation_db is None:
            raise EntityNotFoundException(plantation.plantation_name, "Plantation")

        await self.db.delete(plantation_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(plantation.plantation_name, "Plantation")

    async def change_visibility(self, plantation: PlantationUpdate) -> Plantation:
        plantation_db = await self.db.get(PlantationDB, plantation.plantation_name)

        if plantation_db is None:
            raise EntityNotFoundException(plantation.plantation_name, "Plantation")

        plantation_db.visible = not plantation_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(plantation_db)

            plantation_dto = Plantation.model_validate(plantation_db)
            return plantation_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(plantation.plantation_name, "Plantation")

    async def commit(self) -> None:
        await self.db.commit()
