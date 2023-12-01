import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.flower_in_box.dto.flower_in_box import FlowerInBox
from src.application.flower_in_box.dto.flower_in_box_create import FlowerInBoxCreate
from src.application.flower_in_box.dto.flower_in_box_update import FlowerInBoxUpdate
from src.application.flower_in_box.interfaces.flower_in_box_mutator import FlowerInBoxMutator

from src.infra.database.models.flower import FlowerInBox as FlowerInBoxDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException, EntityUpdateException,
)


class Mutator(BaseRepo, FlowerInBoxMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, flower: FlowerInBoxCreate) -> FlowerInBox:
        new_flower = FlowerInBoxDB()
        mutate_entity(new_flower, flower)

        try:
            self.db.add(new_flower)
            await self.db.flush()
            await self.db.refresh(new_flower)

            flower_dto = FlowerInBox.model_validate(new_flower)
            return flower_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(flower)

    async def update(self, flower_id: uuid.UUID, flower: FlowerInBoxUpdate) -> FlowerInBox:
        flower_in_box_db = await self.db.get(FlowerInBoxDB, flower_id)

        if flower_in_box_db is None:
            raise EntityNotFoundException(str(flower_id), "Client")

        mutate_entity(flower_in_box_db, flower)

        try:
            await self.db.flush()
            await self.db.refresh(flower_in_box_db)

            client_dto = FlowerInBox.model_validate(flower_in_box_db)
            return client_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(flower)

    async def delete(self, flower_id: uuid.UUID) -> FlowerInBox:
        flower_db = await self.db.get(FlowerInBoxDB, flower_id)

        if flower_db is None:
            raise EntityNotFoundException(flower_id, "FlowerInBox")

        await self.db.delete(flower_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(flower_id, "FlowerInBox")

    async def change_visibility(self, flower_in_box: FlowerInBoxUpdate) -> FlowerInBox:
        flower_db = await self.db.get(FlowerInBoxDB, flower_in_box.flower_name)

        if flower_db is None:
            raise EntityNotFoundException(flower_in_box.flower_name, "FlowerInBox")

        flower_db.visible = not flower_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(flower_db)

            flower_dto = FlowerInBox.model_validate(flower_db)
            return flower_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(flower_in_box.flower_name, "FlowerInBox")

    async def commit(self) -> None:
        await self.db.commit()
