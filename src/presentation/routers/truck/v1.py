from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.truck_create import TruckCreate
from src.application.enums.truck.dto.truck_update import TruckUpdate
from src.application.enums.truck.dto.trucks import Trucks
from src.infra.database.repositories.truck.mutator import Mutator
from src.infra.database.repositories.truck.reader import Reader
from src.presentation.routers.dependencies import get_session

trucks = APIRouter(prefix="/trucks", tags=["trucks"])


@trucks.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Truck},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_truck(
    truck_create: TruckCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_truck = await mutator.add(truck_create)
    await mutator.commit()
    return created_truck


@trucks.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": Truck},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_truck(
    truck_update: TruckUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_truck = await mutator.change_visibility(truck=truck_update)
    await mutator.commit()
    return updated_truck


@trucks.delete(
    path="/delete",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_truck(
        truck: TruckUpdate,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_truck = await mutator.delete(truck=truck)
    await mutator.commit()
    return deleted_truck


@trucks.get(
    path="/name/{truck_name}",
    responses={
        status.HTTP_200_OK: {"model": Truck},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_truck(
    truck_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    truck = await reader.get_by_name(truck_name=truck_name)
    return truck


@trucks.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_trucks_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@trucks.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Trucks},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_trucks(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_trucks = await reader.get_trucks(filters=filters)
    return filtered_trucks


@trucks.get(
    path="/exists/name/{truck_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def truck_exists_by_name(
    truck_name: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_name(truck_name)
    return exists
