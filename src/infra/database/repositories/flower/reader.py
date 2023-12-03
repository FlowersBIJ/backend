from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flowers import Flowers
from src.application.enums.flower.interfaces.flower_reader import FlowerReader
from src.infra.database.models.flower import Flower as FlowerDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, FlowerReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, flower_name: str) -> Flower:
        flower_db = await self.db.get(FlowerDB, flower_name)

        if flower_db is None:
            raise EntityNotFoundException(flower_name, "Flower")

        flower_dto = Flower.model_validate(flower_db)

        return flower_dto

    async def get_flowers(self, filters: Filters) -> Flowers:
        query = select(FlowerDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerDB.flower_name.asc())
        else:
            query = query.order_by(FlowerDB.flower_name.desc())

        if filters.visible is not None:
            query = query.where(FlowerDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Flower.model_validate(result) for result in results]
        return Flowers(
            flowers=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(FlowerDB)
        if visible:
            q = q.where(FlowerDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_name(self, flower_name: str) -> bool:
        query = select(exists(FlowerDB).where(FlowerDB.flower_name == flower_name))
        return bool(await self.db.scalar(query))
