from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flower_create import FlowerCreate
from src.application.enums.flower.dto.flower_update import FlowerUpdate
from src.application.enums.flower.interfaces.flower_mutator import FlowerMutator
from src.infra.database.models.flower import Flower as FlowerDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityVisibilityChangeException,
)


class Mutator(BaseRepo, FlowerMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, flower: FlowerCreate) -> Flower:
        new_flower = FlowerDB()
        mutate_entity(new_flower, flower)

        try:
            self.db.add(new_flower)
            await self.db.flush()
            await self.db.refresh(new_flower)

            flower_dto = Flower.model_validate(new_flower)
            return flower_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(flower)

    async def delete(self, flower: FlowerUpdate) -> None:
        flower_db = await self.db.get(FlowerDB, flower.flower_name)

        if flower_db is None:
            raise EntityNotFoundException(flower.flower_name, "Flower")

        await self.db.delete(flower_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(flower.flower_name, "Flower")

    async def change_visibility(self, flower: FlowerUpdate) -> Flower:
        flower_db = await self.db.get(FlowerDB, flower.flower_name)

        if flower_db is None:
            raise EntityNotFoundException(flower.flower_name, "Flower")

        flower_db.visible = not flower_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(flower_db)

            flower_dto = Flower.model_validate(flower_db)
            return flower_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(flower.flower_name, "Flower")

    async def commit(self) -> None:
        await self.db.commit()
