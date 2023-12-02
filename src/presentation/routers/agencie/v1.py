from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencie_create import AgencieCreate
from src.application.enums.agencie.dto.agencie_update import AgencieUpdate
from src.application.enums.agencie.dto.agencies import Agencies
from src.infra.database.repositories.agencie.mutator import Mutator
from src.infra.database.repositories.agencie.reader import Reader
from src.presentation.routers.dependencies import get_session

agencies = APIRouter(prefix="/agencies", tags=["agencies"])


@agencies.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Agencie},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_agencie(
    agencie_create: AgencieCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_agencie = await mutator.add(agencie_create)
    await mutator.commit()
    return created_agencie


@agencies.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": Agencie},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_agencie(
    agencie_update: AgencieUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_agencie = await mutator.change_visibility(agencie=agencie_update)
    await mutator.commit()
    return updated_agencie


@agencies.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_agencie(
    agencie: AgencieUpdate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(agencie=agencie)
    await mutator.commit()


@agencies.get(
    path="/name/{agencie_name}",
    responses={
        status.HTTP_200_OK: {"model": Agencie},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_agencie(
    agencie_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    agencie = await reader.get_by_name(agencie_name=agencie_name)
    return agencie


@agencies.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_agencies_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@agencies.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Agencies},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_agencies(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_agencies = await reader.get_agencies(filters=filters)
    return filtered_agencies


@agencies.get(
    path="/exists/name/{agencie_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def agencie_exists_by_name(
    agencie_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(agencie_name)
    return exists
