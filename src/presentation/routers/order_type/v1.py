from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_type_create import OrderTypeCreate
from src.application.enums.order_type.dto.order_type_update import OrderTypeUpdate
from src.application.enums.order_type.dto.order_types import OrderTypes
from src.infra.database.repositories.order_type.mutator import Mutator
from src.infra.database.repositories.order_type.reader import Reader
from src.presentation.routers.dependencies import get_session

order_types = APIRouter(prefix="/order_types", tags=["order_types"])


@order_types.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": OrderType},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_order_type(
    order_type_create: OrderTypeCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_order_type = await mutator.add(order_type_create)
    await mutator.commit()
    return created_order_type


@order_types.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": OrderType},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_order_type(
    order_type_update: OrderTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_order_type = await mutator.change_visibility(order_type_update)
    await mutator.commit()
    return updated_order_type


@order_types.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_order_type(
    order_type: OrderTypeUpdate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(order_type)
    await mutator.commit()


@order_types.get(
    path="/name/{order_type_name}",
    responses={
        status.HTTP_200_OK: {"model": OrderType},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_order_type(
    order_type_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    order_type = await reader.get_by_name(typename=order_type_name)
    return order_type


@order_types.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_order_types_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@order_types.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": OrderTypes},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_order_types(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_order_types = await reader.get_types(filters=filters)
    return filtered_order_types


@order_types.get(
    path="/exists/name/{order_type_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def order_type_exists_by_name(
    order_type_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(order_type_name)
    return exists
