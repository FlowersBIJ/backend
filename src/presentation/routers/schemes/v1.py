from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.scheme_create import SchemeCreate
from src.application.scheme.dto.scheme_update import SchemeUpdate
from src.infra.database.repositories.scheme.mutator import Mutator
from src.infra.database.repositories.scheme.reader import Reader
from src.presentation.routers.dependencies import get_session

schemes = APIRouter(prefix="/schemes", tags=["schemes"])


@schemes.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Scheme},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_scheme(
    scheme_create: SchemeCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_scheme = await mutator.add(scheme_create)
    await mutator.commit()
    return created_scheme


@schemes.put(
    path="/id/{scheme_id}",
    responses={
        status.HTTP_200_OK: {"model": Scheme},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_scheme(
    scheme_id: UUID,
    scheme_update: SchemeUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(scheme_id=scheme_id, scheme=scheme_update)
    await mutator.commit()
    return updated_scheme


@schemes.delete(
    path="/id/{scheme_id}",
    responses={
        status.HTTP_200_OK: {"model": Scheme},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_scheme(
    scheme_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_scheme = await mutator.delete(scheme_id=scheme_id)
    await mutator.commit()
    return deleted_scheme


@schemes.get(
    path="/id/{scheme_id}",
    responses={
        status.HTTP_200_OK: {"model": Scheme},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_scheme(
    scheme_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    scheme = await reader.get_by_id(scheme_id=scheme_id)
    return scheme


@schemes.get(
    path="/name/{scheme_name}",
    responses={
        status.HTTP_200_OK: {"model": Scheme},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_scheme_by_name(
    scheme_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    scheme = await reader.get_by_name(scheme_name)
    return scheme


@schemes.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_schemes_count(
    session: Annotated[AsyncSession, Depends(get_session)], deleted: bool = False
):
    reader = Reader(session)
    count = await reader.get_count(deleted)
    return count


@schemes.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": list[Scheme]},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_schemes(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_schemes = await reader.get_schemes(filters=filters)
    return filtered_schemes


@schemes.get(
    path="/exists/id/{scheme_id}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def scheme_exists_by_id(
    scheme_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_id(scheme_id)
    return exists


@schemes.get(
    path="/exists/name/{scheme_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def scheme_exists_by_name(
    scheme_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(scheme_name)
    return exists
