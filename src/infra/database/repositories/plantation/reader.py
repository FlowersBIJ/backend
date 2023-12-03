from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantations import Plantations
from src.application.enums.plantation.interfaces.plantation_reader import (
    PlantationReader,
)
from src.infra.database.models.box import Plantation as PlantationDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, PlantationReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, plantation_name: str) -> Plantation:
        plantation_db = await self.db.get(PlantationDB, plantation_name)

        if plantation_db is None:
            raise EntityNotFoundException(plantation_name, "Plantation")

        plantation_dto = Plantation.model_validate(plantation_db)

        return plantation_dto

    async def get_plantations(self, filters: Filters) -> Plantations:
        query = select(PlantationDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(PlantationDB.plantation_name.asc())
        else:
            query = query.order_by(PlantationDB.plantation_name.desc())

        if filters.visible is not None:
            query = query.where(PlantationDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Plantation.model_validate(result) for result in results]
        return Plantations(
            plantations=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(PlantationDB)
        if visible:
            q = q.where(PlantationDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_name(self, plantation_name: str) -> bool:
        query = select(
            exists(PlantationDB).where(PlantationDB.plantation_name == plantation_name)
        )
        return bool(await self.db.scalar(query))
