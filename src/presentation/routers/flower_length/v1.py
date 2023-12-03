from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flower_length_create import (
    FlowerLengthCreate,
)
from src.application.enums.flower_length.dto.flower_length_update import (
    FlowerLengthUpdate,
)
from src.application.enums.flower_length.dto.flowers_length import FlowersLength
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.flower_length.mutator import Mutator
from src.infra.database.repositories.flower_length.reader import Reader
from src.presentation.routers.dependencies import get_session

flowers_length = APIRouter(prefix="/flower_lengths", tags=["flower_lengths"])


@flowers_length.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowerLength},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_flower_length(
    flower_length_create: FlowerLengthCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_flower_length = await mutator.add(flower_length_create)
    await mutator.commit()
    return created_flower_length


@flowers_length.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": FlowerLength},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_flower_length(
    flower_length: FlowerLengthUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_flower_length = await mutator.change_visibility(flower_length)
    await mutator.commit()
    return updated_flower_length


@flowers_length.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_flower_length(
    flower_length: FlowerLengthUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    await mutator.delete(flower_length)
    await mutator.commit()


@flowers_length.get(
    path="/name/{flower_name}/sort/{flower_sort}",
    responses={
        status.HTTP_200_OK: {"model": FlowersLength},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flower_length_by_name_and_sort(
    flower_name: str,
    flower_sort: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Filters = Depends(),
):
    reader = Reader(session)
    flower_length = await reader.get_by_flower_name_and_sort(
        flower_name=flower_name, flower_sort=flower_sort, filters=filters
    )
    return flower_length


@flowers_length.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_flower_lengths_count(
    session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    count = await reader.get_count()
    return count


@flowers_length.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowersLength},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flowers_length(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_flower_lengths = await reader.get_all(filters=filters)
    return filtered_flower_lengths


@flowers_length.get(
    path="/exists/sort",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def flower_length_exists_by_name(
    flower_length: FlowerLength, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_sort(flower_length)
    return exists
