from uuid import UUID

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.box.dto.box import Box
from src.application.box.dto.boxes import Boxes
from src.application.box.interfaces.box_reader import BoxReader
from src.application.common.filters.filter import Filters, OrderFilter
from src.infra.database.models.box import Box as BoxDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, BoxReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_id(self, box_id: UUID) -> Box:
        box_db = await self.db.get(BoxDB, box_id)

        if box_db is None:
            raise EntityNotFoundException(str(box_id), "Box")

        box_dto = Box.model_validate(box_db)

        return box_dto

    async def get_boxes(self, filters: Filters) -> Boxes:
        query = select(BoxDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(BoxDB.id.asc())
        else:
            query = query.order_by(BoxDB.id.desc())

        if filters.visible is not None:
            query = query.where(BoxDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Box.model_validate(result) for result in results]
        return Boxes(
            boxes=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(BoxDB)
        if visible:
            q = q.where(BoxDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_id(self, box_id: UUID) -> bool:
        query = select(exists(BoxDB).where(BoxDB.id == box_id))
        return bool(await self.db.scalar(query))
