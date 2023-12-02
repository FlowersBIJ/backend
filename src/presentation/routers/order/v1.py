import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.order.dto.order import Order
from src.application.order.dto.order_create import OrderCreate
from src.application.order.dto.order_update import OrderUpdate
from src.application.order.dto.orders import Orders
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.order.mutator import Mutator
from src.infra.database.repositories.order.reader import Reader
from src.presentation.routers.dependencies import get_session

orders = APIRouter(prefix="/orders", tags=["orders"])


@orders.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Order},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_order(
        order_create: OrderCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_order = await mutator.add(order_create)
    await mutator.commit()
    return created_order


@orders.put(
    path="/change_visibility/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": Order},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_order(
        order_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_order = await mutator.change_visibility(order_id)
    await mutator.commit()
    return updated_order


@orders.delete(
    path="/delete/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_order(
        order_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_order = await mutator.delete(order_id)
    await mutator.commit()
    return deleted_order


@orders.put(
    path="/id/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": Order},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_order(
        order_id: uuid.UUID,
        order_update: OrderUpdate,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(order_id, order_update)
    await mutator.commit()
    return updated_scheme


@orders.get(
    path="/id/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": Order},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_order(
        order_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    order = await reader.get_by_id(order_id)
    return order


@orders.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_orders_count(
        session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@orders.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Orders},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_orders(
        session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_orders = await reader.get_orders(filters=filters)
    return filtered_orders


@orders.get(
    path="/exists/id/{order_id}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def order_exists_by_name(
        order_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_id(order_id)
    return exists
