from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flower_sort_create import FlowerSortCreate
from src.application.enums.flower_sort.dto.flower_sort_update import FlowerSortUpdate
from src.application.enums.flower_sort.interfaces.flower_sort_mutator import (
    FlowerSortMutator,
)

from src.infra.database.models.flower import FlowerSort as FlowerSortDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityVisibilityChangeException,
)


class Mutator(BaseRepo, FlowerSortMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, flower: FlowerSortCreate) -> FlowerSort:
        new_flower = FlowerSortDB()
        mutate_entity(new_flower, flower)

        try:
            self.db.add(new_flower)
            await self.db.flush()
            await self.db.refresh(new_flower)

            flower_dto = FlowerSort.model_validate(new_flower)
            return flower_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(flower)

    async def delete(self, flower_sort: FlowerSortUpdate) -> None:
        flower_db = await self.db.get(
            FlowerSortDB, (flower_sort.flower_name, flower_sort.flower_sort)
        )

        if flower_db is None:
            raise EntityNotFoundException(f"{flower_sort.flower_name} - {flower_sort.flower_sort}", "FlowerSort")

        await self.db.delete(flower_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(f"{flower_sort.flower_name} - {flower_sort.flower_sort}", "FlowerSort")

    async def change_visibility(self, flower_sort: FlowerSortUpdate) -> FlowerSort:
        flower_db = await self.db.get(FlowerSortDB, (flower_sort.flower_name, flower_sort.flower_sort))

        if flower_db is None:
            raise EntityNotFoundException(f"{flower_sort.flower_name} - {flower_sort.flower_sort}", "FlowerSort")

        flower_db.visible = not flower_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(flower_db)

            flower_dto = FlowerSort.model_validate(flower_db)
            return flower_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(f"{flower_sort.flower_name} - {flower_sort.flower_sort}", "FlowerSort")

    async def commit(self) -> None:
        await self.db.commit()
