from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_types import OrderTypes
from src.application.enums.order_type.interfaces.order_type_reader import OrderTypeReader
from src.infra.database.models.order import OrderType as OrderTypeDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, OrderTypeReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, typename: str) -> OrderType:
        order_type_db = await self.db.get(OrderTypeDB, typename)

        if order_type_db is None:
            raise EntityNotFoundException(typename, "OrderType")

        order_type_dto = OrderType.model_validate(order_type_db)

        return order_type_dto

    async def get_types(self, filters: Filters) -> OrderTypes:
        query = select(OrderTypeDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(OrderTypeDB.typename.asc())
        else:
            query = query.order_by(OrderTypeDB.typename.desc())

        if filters.visible is not None:
            query = query.where(OrderTypeDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [OrderType.model_validate(result) for result in results]
        return OrderTypes(
            types=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(OrderTypeDB)
        if visible:
            q = q.where(OrderTypeDB.visible == visible)
        return (
            await self.db.scalar(q)
        ) or 0

    async def check_exists_by_name(self, typename: str) -> bool:
        query = select(exists(OrderTypeDB).where(OrderTypeDB.typename == typename))
        return bool(await self.db.scalar(query))
