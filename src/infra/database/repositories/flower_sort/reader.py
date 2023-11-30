from sqlalchemy import select, exists, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flowers_sorts import FlowersSorts
from src.application.enums.flower_sort.interfaces.flower_sort_reader import FlowerSortReader
from src.infra.database.models.flower import FlowerSort as FlowerSortDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, FlowerSortReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_flower_name(self, flower_name: str, filters: Filters) -> FlowersSorts:
        query = select(FlowerSortDB).where(FlowerSortDB.flower_name == flower_name)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerSortDB.flower_name.asc())
        else:
            query = query.order_by(FlowerSortDB.flower_name.desc())

        if filters.visible is not None:
            query = query.where(FlowerSortDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [FlowerSort.model_validate(result) for result in results]
        return FlowersSorts(
            flowers_sorts=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_all(self, filters: Filters) -> FlowersSorts:
        query = select(FlowerSortDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerSortDB.flower_name.asc())
        else:
            query = query.order_by(FlowerSortDB.flower_name.desc())

        if filters.visible is not None:
            query = query.where(FlowerSortDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [FlowerSort.model_validate(result) for result in results]
        return FlowersSorts(
            flowers_sorts=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(FlowerSortDB)
        if visible:
            q = q.where(FlowerSortDB.visible == visible)
        return (
            await self.db.scalar(q)
        ) or 0

    async def check_exists_by_sort(self, sort: FlowerSort) -> bool:
        query = select(exists(FlowerSortDB).where(
            and_(
                FlowerSortDB.flower_name == sort.flower_name,
                FlowerSortDB.flower_sort == sort.flower_sort,
            )
        ))
        return bool(await self.db.scalar(query))
