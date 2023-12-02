import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.order.dto.order import Order
from src.application.order.dto.order_create import OrderCreate
from src.application.order.dto.order_update import OrderUpdate
from src.application.order.interfaces.order_mutator import OrderMutator
from src.infra.database.models.order import Order as OrderDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityVisibilityChangeException,
    EntityUpdateException,
)


class Mutator(BaseRepo, OrderMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, order: OrderCreate) -> Order:
        new_order = OrderDB()
        mutate_entity(new_order, order)

        try:
            self.db.add(new_order)
            await self.db.flush()
            await self.db.refresh(new_order)

            order_dto = Order.model_validate(new_order)
            return order_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(order)

    async def update(self, order_id: uuid.UUID, order: OrderUpdate) -> Order:
        order_db = await self.db.get(OrderDB, order_id)

        if order_db is None:
            raise EntityNotFoundException(str(order_id), "Order")

        mutate_entity(order_db, order)

        try:
            await self.db.flush()
            await self.db.refresh(order_db)

            order_dto = Order.model_validate(order_db)
            return order_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(order)

    async def delete(self, order_id: uuid.UUID) -> None:
        order_db = await self.db.get(OrderDB, order_id)

        if order_db is None:
            raise EntityNotFoundException(str(order_id), "Order")

        await self.db.delete(order_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(order_id), "Order")

    async def change_visibility(self, order_id: uuid.UUID) -> Order:
        order_db = await self.db.get(OrderDB, order_id)

        if order_db is None:
            raise EntityNotFoundException(str(order_id), "Order")

        order_db.visible = not order_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(order_db)

            order_dto = Order.model_validate(order_db)
            return order_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(str(order_id), "Order")

    async def commit(self) -> None:
        await self.db.commit()
