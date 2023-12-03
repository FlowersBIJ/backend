from uuid import UUID

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_types import BoxTypes
from src.infra.database.models.box import BoxType as BoxTypeDB
from src.application.enums.box_type.interfaces.box_type_reader import BoxTypeReader
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, BoxTypeReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, typename: str) -> BoxType:
        box_type_db = await self.db.get(BoxTypeDB, typename)

        if box_type_db is None:
            raise EntityNotFoundException(typename, "BoxType")

        box_type_dto = BoxType.model_validate(box_type_db)

        return box_type_dto

    async def get_types(self, filters: Filters) -> BoxTypes:
        query = select(BoxTypeDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(BoxTypeDB.typename.asc())
        else:
            query = query.order_by(BoxTypeDB.typename.desc())

        if filters.visible is not None:
            query = query.where(BoxTypeDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [BoxType.model_validate(result) for result in results]
        return BoxTypes(
            box_types=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(BoxTypeDB)
        if visible:
            q = q.where(BoxTypeDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_name(self, typename: str) -> bool:
        query = select(exists(BoxTypeDB).where(BoxTypeDB.typename == typename))
        return bool(await self.db.scalar(query))
