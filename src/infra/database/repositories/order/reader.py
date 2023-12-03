import uuid

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.order.dto.order import Order
from src.application.order.dto.orders import Orders
from src.application.order.interfaces.order_reader import OrderReader
from src.infra.database.models.order import Order as OrderDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, OrderReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_id(self, order_id: uuid.UUID) -> Order:
        order_db = await self.db.get(OrderDB, order_id)

        if order_db is None:
            raise EntityNotFoundException(str(order_id), "Order")

        order_dto = Order.model_validate(order_db)

        return order_dto

    async def get_orders(self, filters: Filters) -> Orders:
        query = select(OrderDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(OrderDB.id.asc())
        else:
            query = query.order_by(OrderDB.id.desc())

        if filters.visible is not None:
            query = query.where(OrderDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Order.model_validate(result) for result in results]
        return Orders(
            orders=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible,
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(OrderDB)
        if visible:
            q = q.where(OrderDB.visible == visible)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_id(self, order_id: uuid.UUID) -> bool:
        query = select(exists(OrderDB).where(OrderDB.id == order_id))
        return bool(await self.db.scalar(query))
