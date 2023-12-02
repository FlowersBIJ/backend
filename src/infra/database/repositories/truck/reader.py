from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.trucks import Trucks
from src.application.enums.truck.interfaces.truck_reader import TruckReader
from src.infra.database.models.client import Truck as TruckDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, TruckReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, truck_name: str) -> Truck:
        truck_db = await self.db.get(TruckDB, truck_name)

        if truck_db is None:
            raise EntityNotFoundException(truck_name, "Truck")

        truck_dto = Truck.model_validate(truck_db)

        return truck_dto

    async def get_trucks(self, filters: Filters) -> Trucks:
        query = select(TruckDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(TruckDB.truck_name.asc())
        else:
            query = query.order_by(TruckDB.truck_name.desc())

        if filters.visible is not None:
            query = query.where(TruckDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Truck.model_validate(result) for result in results]
        return Trucks(
            trucks=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(TruckDB)
        if visible:
            q = q.where(TruckDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_name(self, truck_name: str) -> bool:
        query = select(exists(TruckDB).where(TruckDB.truck_name == truck_name))
        return bool(await self.db.scalar(query))
