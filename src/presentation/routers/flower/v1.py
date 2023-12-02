from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flower_create import FlowerCreate
from src.application.enums.flower.dto.flower_update import FlowerUpdate
from src.application.enums.flower.dto.flowers import Flowers
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.flower.mutator import Mutator
from src.infra.database.repositories.flower.reader import Reader
from src.presentation.routers.dependencies import get_session

flowers = APIRouter(prefix="/flowers", tags=["flowers"])


@flowers.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Flower},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_flower(
    flower_create: FlowerCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_flower = await mutator.add(flower_create)
    await mutator.commit()
    return created_flower


@flowers.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": Flower},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_flower(
    flower: FlowerUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_flower = await mutator.change_visibility(flower)
    await mutator.commit()
    return updated_flower


@flowers.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_flower(
    flower: FlowerUpdate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(flower)
    await mutator.commit()


@flowers.get(
    path="/name/{flower_name}",
    responses={
        status.HTTP_200_OK: {"model": Flower},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flower(
    flower_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    flower = await reader.get_by_name(flower_name)
    return flower


@flowers.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_flowers_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@flowers.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Flowers},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flowers(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_flowers = await reader.get_flowers(filters=filters)
    return filtered_flowers


@flowers.get(
    path="/exists/name/{flower_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def flower_exists_by_name(
    flower_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(flower_name)
    return exists
