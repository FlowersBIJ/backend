import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_type_create import BoxTypeCreate
from src.application.enums.box_type.dto.box_type_update import BoxTypeUpdate
from src.application.enums.box_type.dto.box_types import BoxTypes
from src.infra.database.repositories.box_type.mutator import Mutator
from src.infra.database.repositories.box_type.reader import Reader
from src.presentation.routers.dependencies import get_session

box_types = APIRouter(prefix="/box_types", tags=["box_types"])


@box_types.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": BoxType},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_box_type(
    box_type_create: BoxTypeCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_box_type = await mutator.add(box_type_create)
    await mutator.commit()
    return created_box_type


@box_types.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": BoxType},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_box_type(
    box_type_update: BoxTypeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_box_type = await mutator.change_visibility(box=box_type_update)
    await mutator.commit()
    return updated_box_type


@box_types.delete(
    path="/delete/{box_type_id}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_box_type(
    box: BoxTypeUpdate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(box)
    await mutator.commit()


@box_types.get(
    path="/name/{box_type_name}",
    responses={
        status.HTTP_200_OK: {"model": BoxType},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_box_type(
    box_type_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    box_type = await reader.get_by_name(typename=box_type_name)
    return box_type


@box_types.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_box_types_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@box_types.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": BoxTypes},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_box_types(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_box_types = await reader.get_types(filters=filters)
    return filtered_box_types


@box_types.get(
    path="/exists/name/{box_type_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def box_type_exists_by_name(
    box_type_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(box_type_name)
    return exists
