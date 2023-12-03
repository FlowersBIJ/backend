import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.flower_in_box.dto.flowers_in_box import FlowerInBox
from src.application.flower_in_box.dto.flower_in_box_create import FlowerInBoxCreate
from src.application.flower_in_box.dto.flower_in_box_update import FlowerInBoxUpdate
from src.application.flower_in_box.dto.flowers_in_box import FlowersInBox
from src.infra.database.repositories.flower_in_box.mutator import Mutator
from src.infra.database.repositories.flower_in_box.reader import Reader
from src.presentation.routers.dependencies import get_session

flowers_in_box = APIRouter(prefix="/flowers_in_box", tags=["flowers_in_box"])


@flowers_in_box.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowerInBox},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_flowers_in_box(
    flowers_in_box_create: FlowerInBoxCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    created_flowers_in_box = await mutator.add(flowers_in_box_create)
    await mutator.commit()
    return created_flowers_in_box


@flowers_in_box.put(
    path="/change_visibility",
    responses={
        status.HTTP_200_OK: {"model": FlowerInBox},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_flowers_in_box(
    flower_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_flowers_in_box = await mutator.change_visibility(flower_id)
    await mutator.commit()
    return updated_flowers_in_box


@flowers_in_box.delete(
    path="/delete/{flowers_in_box_id}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_flowers_in_box(
    flowers_in_box_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    await mutator.delete(flower_id=flowers_in_box_id)
    await mutator.commit()


@flowers_in_box.put(
    path="/id/{flowers_in_box_id}",
    responses={
        status.HTTP_200_OK: {"model": FlowerInBox},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_flowers_in_box(
    flowers_in_box_id: uuid.UUID,
    flowers_in_box_update: FlowerInBoxUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(
        flower_id=flowers_in_box_id, flower=flowers_in_box_update
    )
    await mutator.commit()
    return updated_scheme


@flowers_in_box.get(
    path="/id/{flowers_in_box_id}",
    responses={
        status.HTTP_200_OK: {"model": FlowerInBox},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flowers_in_box(
    flowers_in_box_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    flowers_in_box_ = await reader.get_by_id(flower_id=flowers_in_box_id)
    return flowers_in_box_


@flowers_in_box.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_flowers_in_boxes_count(
    session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@flowers_in_box.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": FlowersInBox},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_flowers_in_boxes(
    session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_flowers_in_boxs = await reader.get_flowers(filters=filters)
    return filtered_flowers_in_boxs


@flowers_in_box.get(
    path="/exists/name/{flowers_in_box_id}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def flowers_in_box_exists_by_name(
    flowers_in_box_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_id(flowers_in_box_id)
    return exists
