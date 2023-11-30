import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filters.filter import Filters
from src.application.box.dto.box import Box
from src.application.box.dto.box_create import BoxCreate
from src.application.box.dto.box_update import BoxUpdate
from src.application.box.dto.boxes import Boxes
from src.infra.database.repositories.box.mutator import Mutator
from src.infra.database.repositories.box.reader import Reader
from src.presentation.routers.dependencies import get_session

boxes = APIRouter(prefix="/boxes", tags=["boxes"])


@boxes.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Box},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_box(
        box_create: BoxCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_box = await mutator.add(box_create)
    await mutator.commit()
    return created_box


@boxes.put(
    path="/change_visibility/{box_id}",
    responses={
        status.HTTP_200_OK: {"model": Box},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_box(
        box_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_box = await mutator.change_visibility(box_id=box_id)
    await mutator.commit()
    return updated_box


@boxes.delete(
    path="/delete/{box_id}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_box(
        box_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_box = await mutator.delete(box_id=box_id)
    await mutator.commit()
    return deleted_box


@boxes.put(
    path="/id/{box_id}",
    responses={
        status.HTTP_200_OK: {"model": Box},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_box(
        box_id: uuid.UUID,
        box_update: BoxUpdate,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(box_id=box_id, box=box_update)
    await mutator.commit()
    return updated_scheme


@boxes.get(
    path="/id/{box_id}",
    responses={
        status.HTTP_200_OK: {"model": Box},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_box(
        box_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    box = await reader.get_by_id(box_id=box_id)
    return box


@boxes.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_boxes_count(
        session: Annotated[AsyncSession, Depends(get_session)], visible: bool | None = None
):
    reader = Reader(session)
    count = await reader.get_count(visible)
    return count


@boxes.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Boxes},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_boxes(
        session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_boxs = await reader.get_boxes(filters=filters)
    return filtered_boxs


@boxes.get(
    path="/exists/name/{box_id}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def box_exists_by_name(
        box_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_id(box_id)
    return exists
