from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.box.dto.box import Box
from src.application.box.dto.box_update import BoxUpdate
from src.infra.database.models.box import Box as BoxDB
from src.application.box.dto.box_create import BoxCreate
from src.application.box.interfaces.box_mutator import BoxMutator
from src.application.common.entity_mutator import mutate_entity
from src.infra.database.repositories.base import BaseRepo

from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityUpdateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityVisibilityChangeException,
)


class Mutator(BaseRepo, BoxMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, box: BoxCreate) -> Box:
        new_box = BoxDB()
        mutate_entity(new_box, box)

        try:
            self.db.add(new_box)
            await self.db.flush()
            await self.db.refresh(new_box)

            box_dto = Box.model_validate(new_box)
            return box_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(box)

    async def update(self, box_id: UUID, box: BoxUpdate) -> Box:
        box_db = await self.db.get(BoxDB, box_id)

        if box_db is None:
            raise EntityNotFoundException(str(box_id), "Box")

        mutate_entity(box_db, box)

        try:
            await self.db.flush()
            await self.db.refresh(box_db)

            box_dto = Box.model_validate(box_db)
            return box_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(box)

    async def delete(self, box_id: UUID) -> None:
        box_db = await self.db.get(BoxDB, box_id)

        if box_db is None:
            raise EntityNotFoundException(str(box_id), "Box")

        await self.db.delete(box_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(box_id), "Box")

    async def change_visibility(self, box_id: UUID) -> Box:
        box_db = await self.db.get(BoxDB, box_id)

        if box_db is None:
            raise EntityNotFoundException(str(box_id), "Box")

        box_db.visible = not box_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(box_db)

            box_dto = Box.model_validate(box_db)
            return box_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(str(box_id), "Box")

    async def commit(self) -> None:
        await self.db.commit()
