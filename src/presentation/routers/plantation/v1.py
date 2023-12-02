from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantation_create import PlantationCreate
from src.application.enums.plantation.dto.plantation_update import PlantationUpdate
from src.application.enums.plantation.dto.plantations import Plantations
from src.infra.database.repositories.plantation.mutator import Mutator
from src.infra.database.repositories.plantation.reader import Reader
from src.presentation.routers.dependencies import get_session

plantations = APIRouter(prefix="/plantations", tags=["plantations"])


@plantations.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Plantation},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_plantation(
    plantation_create: PlantationCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_plantation = await mutator.add(plantation_create)
    await mutator.commit()
    return created_plantation


@plantations.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": Plantation},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_plantation(
    plantation_update: PlantationUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_plantation = await mutator.change_visibility(plantation=plantation_update)
    await mutator.commit()
    return updated_plantation


@plantations.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_plantation(
    plantation: PlantationUpdate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(plantation=plantation)
    await mutator.commit()


@plantations.get(
    path="/name/{plantation_name}",
    responses={
        status.HTTP_200_OK: {"model": Plantation},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_plantation(
    plantation_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    plantation = await reader.get_by_name(plantation_name=plantation_name)
    return plantation


@plantations.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_plantations_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@plantations.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Plantations},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_plantations(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_plantations = await reader.get_plantations(filters=filters)
    return filtered_plantations


@plantations.get(
    path="/exists/name/{plantation_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def plantation_exists_by_name(
    plantation_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(plantation_name)
    return exists
