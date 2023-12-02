from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_type_create import OrderTypeCreate
from src.application.enums.order_type.dto.order_type_update import OrderTypeUpdate
from src.application.enums.order_type.interfaces.order_type_mutator import (
    OrderTypeMutator,
)
from src.infra.database.models.order import OrderType as OrderTypeDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityVisibilityChangeException,
)


class Mutator(BaseRepo, OrderTypeMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, order_type: OrderTypeCreate) -> OrderType:
        new_order_type = OrderTypeDB()
        mutate_entity(new_order_type, order_type)

        try:
            self.db.add(new_order_type)
            await self.db.flush()
            await self.db.refresh(new_order_type)

            order_type_dto = OrderType.model_validate(new_order_type)
            return order_type_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(order_type)

    async def delete(self, order: OrderTypeUpdate) -> None:
        order_type_db = await self.db.get(OrderTypeDB, order.typename)

        if order_type_db is None:
            raise EntityNotFoundException(str(order.typename), "OrderType")

        await self.db.delete(order_type_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(order.typename), "OrderType")

    async def change_visibility(self, order: OrderTypeUpdate) -> OrderType:
        order_type_db = await self.db.get(OrderTypeDB, order.typename)

        if order_type_db is None:
            raise EntityNotFoundException(str(order.typename), "OrderType")

        order_type_db.visible = not order_type_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(order_type_db)

            order_type_dto = OrderType.model_validate(order_type_db)
            return order_type_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(order.typename, "OrderType")

    async def commit(self) -> None:
        await self.db.commit()
