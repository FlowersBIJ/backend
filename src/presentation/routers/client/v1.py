from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.client.dto.client import Client
from src.application.client.dto.client_create import ClientCreate
from src.application.client.dto.client_update import ClientUpdate
from src.application.client.dto.clients import Clients
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.client.mutator import Mutator
from src.infra.database.repositories.client.reader import Reader
from src.presentation.routers.dependencies import get_session

clients = APIRouter(prefix="/clients", tags=["clients"])


@clients.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Client},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_client(
    client_create: ClientCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_client = await mutator.add(client_create)
    await mutator.commit()
    return created_client


@clients.put(
    path="/change_visibility/{client_name}",
    responses={
        status.HTTP_200_OK: {"model": Client},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_client(
    client_name: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_client = await mutator.change_visibility(client_name=client_name)
    await mutator.commit()
    return updated_client


@clients.delete(
    path="/delete/{client_name}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_client(
    client_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(client_name=client_name)
    await mutator.commit()


@clients.put(
    path="/name/{client_name}",
    responses={
        status.HTTP_200_OK: {"model": Client},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_client(
    client_name: str,
    client_update: ClientUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(client_name=client_name, client=client_update)
    await mutator.commit()
    return updated_scheme


@clients.get(
    path="/name/{client_name}",
    responses={
        status.HTTP_200_OK: {"model": Client},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_client(
    client_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    client = await reader.get_by_name(client_name)
    return client


@clients.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_clients_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@clients.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Clients},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_clients(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_clients = await reader.get_clients(filters=filters)
    return filtered_clients


@clients.get(
    path="/exists/name/{client_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def client_exists_by_name(
    client_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(client_name)
    return exists
