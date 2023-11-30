from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flower_sort_create import FlowerSortCreate
from src.application.enums.flower_sort.dto.flower_sort_update import FlowerSortUpdate
from src.application.enums.flower_sort.dto.flowers_sorts import FlowersSorts
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.flower_sort.mutator import Mutator
from src.infra.database.repositories.flower_sort.reader import Reader
from src.presentation.routers.dependencies import get_session

flowers_sort = APIRouter(prefix="/flower_sorts", tags=["flower_sorts"])


@flowers_sort.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowerSort},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_flower_sort(
        flower_sort_create: FlowerSortCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_flower_sort = await mutator.add(flower_sort_create)
    await mutator.commit()
    return created_flower_sort


@flowers_sort.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": FlowerSort},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_flower_sort(
        flower_sort: FlowerSortUpdate,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_flower_sort = await mutator.change_visibility(flower_sort)
    await mutator.commit()
    return updated_flower_sort


@flowers_sort.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_flower_sort(
        flower_sort: FlowerSortUpdate,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_flower_sort = await mutator.delete(flower_sort)
    await mutator.commit()
    return deleted_flower_sort


@flowers_sort.get(
    path="/name/{flower_name}",
    responses={
        status.HTTP_200_OK: {"model": FlowersSorts},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flower_sorts_by_name(
        flower_name: str, session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    flowers_sorts = await reader.get_by_flower_name(
        flower_name=flower_name,
        filters=filters
    )
    return flowers_sorts


@flowers_sort.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_flower_sorts_count(
        session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    count = await reader.get_count()
    return count


@flowers_sort.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowersSorts},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flowers_sorts(
        session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_flower_sorts = await reader.get_all(filters=filters)
    return filtered_flower_sorts


@flowers_sort.get(
    path="/exists/sort",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def flower_sort_exists_by_name(
        flower_sort: FlowerSort, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_sort(flower_sort)
    return exists
