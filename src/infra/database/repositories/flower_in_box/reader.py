import uuid

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.flower_in_box.dto.flowers_in_box import FlowerInBox, FlowersInBox
from src.application.flower_in_box.interfaces.flower_in_box_reader import (
    FlowerInBoxReader,
)
from src.infra.database.models.flower import FlowerInBox as FlowerInBoxDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import EntityNotFoundException


class Reader(BaseRepo, FlowerInBoxReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_id(self, flower_id: uuid.UUID) -> FlowerInBox:
        flower_in_box_db = await self.db.get(FlowerInBoxDB, flower_id)

        if flower_in_box_db is None:
            raise EntityNotFoundException(str(flower_id), "FlowerInBox")

        flower_in_box_dto = FlowerInBox.model_validate(flower_in_box_db)

        return flower_in_box_dto

    async def get_flowers(self, filters: Filters) -> FlowersInBox:
        query = select(FlowerInBoxDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerInBoxDB.flower_name.asc())
        else:
            query = query.order_by(FlowerInBoxDB.flower_name.desc())

        if filters.visible is not None:
            query = query.where(FlowerInBoxDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count()
        dto_list = [FlowerInBox.model_validate(result) for result in results]
        return FlowersInBox(
            flowers=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(FlowerInBoxDB)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_id(self, flower_id: uuid.UUID) -> bool:
        query = select(exists(FlowerInBoxDB).where(FlowerInBoxDB.id == flower_id))
        return bool(await self.db.scalar(query))
