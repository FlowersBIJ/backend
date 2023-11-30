from sqlalchemy import select, exists, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flowers_length import FlowersLength
from src.application.enums.flower_length.interfaces.flower_length_reader import FlowerLengthReader
from src.infra.database.models.flower import FlowerLength as FlowerLengthDB
from src.infra.database.repositories.base import BaseRepo


class Reader(BaseRepo, FlowerLengthReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_flower_name_and_sort(self, flower_name: str, flower_sort: str, filters: Filters) -> FlowersLength:
        query = select(FlowerLengthDB).where(
            and_(
                FlowerLengthDB.flower_name == flower_name,
                FlowerLengthDB.flower_sort == flower_sort
            )
        )
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerLengthDB.flower_name.asc())
        else:
            query = query.order_by(FlowerLengthDB.flower_name.desc())

        # if filters.visible is not None:
        #     query = query.where(FlowerLengthDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count()
        dto_list = [FlowerLength.model_validate(result) for result in results]
        return FlowersLength(
            flowers_length=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_all(self, filters: Filters) -> FlowersLength:
        query = select(FlowerLengthDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(FlowerLengthDB.flower_name.asc())
        else:
            query = query.order_by(FlowerLengthDB.flower_name.desc())

        # if filters.visible is not None:
        #     query = query.where(FlowerLengthDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count()
        dto_list = [FlowerLength.model_validate(result) for result in results]
        return FlowersLength(
            flowers_length=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_count(self) -> int:
        q = select(func.count()).select_from(FlowerLengthDB)
        return (
            await self.db.scalar(q)
        ) or 0

    async def check_exists_by_sort(self, flower_length: FlowerLength) -> bool:
        query = select(exists(FlowerLengthDB).where(
            and_(
                FlowerLengthDB.flower_name == flower_length.flower_name,
                FlowerLengthDB.flower_length == flower_length.flower_length,
            )
        ))
        return bool(await self.db.scalar(query))
