from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flower_length_create import FlowerLengthCreate
from src.application.enums.flower_length.dto.flower_length_update import FlowerLengthUpdate
from src.application.enums.flower_length.interfaces.flower_length_mutator import FlowerLengthMutator

from src.infra.database.models.flower import FlowerLength as FlowerLengthDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, FlowerLengthMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, flower: FlowerLengthCreate) -> FlowerLength:
        new_flower = FlowerLengthDB()
        mutate_entity(new_flower, flower)

        try:
            self.db.add(new_flower)
            await self.db.flush()
            await self.db.refresh(new_flower)

            flower_dto = FlowerLength.model_validate(new_flower)
            return flower_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(flower)

    async def delete(self, flower_length: FlowerLengthUpdate) -> FlowerLength:
        flower_db = await self.db.get(FlowerLengthDB, (flower_length.flower_name, flower_length.flower_length))

        if flower_db is None:
            raise EntityNotFoundException(flower_length.flower_name, "FlowerLength")

        await self.db.delete(flower_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(flower_length.flower_name, "FlowerLength")

    async def change_visibility(self, flower_length: FlowerLengthUpdate) -> FlowerLength:
        flower_db = await self.db.get(FlowerLengthDB, flower_length.flower_name)

        if flower_db is None:
            raise EntityNotFoundException(flower_length.flower_name, "FlowerLength")

        flower_db.visible = not flower_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(flower_db)

            flower_dto = FlowerLength.model_validate(flower_db)
            return flower_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(flower_length.flower_name, "FlowerLength")

    async def commit(self) -> None:
        await self.db.commit()