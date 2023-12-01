from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_type_create import BoxTypeCreate
from src.application.enums.box_type.dto.box_type_update import BoxTypeUpdate
from src.application.enums.box_type.interfaces.box_type_mutator import BoxTypeMutator
from src.infra.database.models.box import BoxType as BoxTypeDB
from src.infra.database.repositories.base import BaseRepo

from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityUpdateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, BoxTypeMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, box_type: BoxTypeCreate) -> BoxType:
        new_box_type = BoxTypeDB()
        mutate_entity(new_box_type, box_type)

        try:
            self.db.add(new_box_type)
            await self.db.flush()
            await self.db.refresh(new_box_type)

            box_type_dto = BoxType.model_validate(new_box_type)
            return box_type_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(box_type)

    async def delete(self, box_type_id: UUID) -> BoxType:
        box_type_db = await self.db.get(BoxTypeDB, box_type_id)

        if box_type_db is None:
            raise EntityNotFoundException(str(box_type_id), "BoxType")

        await self.db.delete(box_type_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(box_type_id), "BoxType")

    async def change_visibility(self, box: BoxTypeUpdate) -> BoxType:
        box_type_db = await self.db.get(BoxTypeDB, box.typename)

        if box_type_db is None:
            raise EntityNotFoundException(str(box.typename), "BoxType")

        box_type_db.visible = not box_type_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(box_type_db)

            box_type_dto = BoxType.model_validate(box_type_db)
            return box_type_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(box.typename, "BoxType")

    async def commit(self) -> None:
        await self.db.commit()
