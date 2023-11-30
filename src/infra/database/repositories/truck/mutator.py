from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.truck_create import TruckCreate
from src.application.enums.truck.dto.truck_update import TruckUpdate
from src.application.enums.truck.interfaces.truck_mutator import TruckMutator
from src.infra.database.models.client import Truck as TruckDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, TruckMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, truck: TruckCreate) -> Truck:
        new_truck = TruckDB()
        mutate_entity(new_truck, truck)

        try:
            self.db.add(new_truck)
            await self.db.flush()
            await self.db.refresh(new_truck)

            truck_dto = Truck.model_validate(new_truck)
            return truck_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(truck)

    async def delete(self, truck: TruckUpdate) -> Truck:
        truck_db = await self.db.get(TruckDB, truck.truck_name)

        if truck_db is None:
            raise EntityNotFoundException(truck.truck_name, "Truck")

        await self.db.delete(truck_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(truck.truck_name, "Truck")

    async def change_visibility(self, truck: TruckUpdate) -> Truck:
        truck_db = await self.db.get(TruckDB, truck.truck_name)

        if truck_db is None:
            raise EntityNotFoundException(truck.truck_name, "Truck")

        truck_db.visible = not truck_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(truck_db)

            truck_dto = Truck.model_validate(truck_db)
            return truck_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(truck.truck_name, "Truck")

    async def commit(self) -> None:
        await self.db.commit()
