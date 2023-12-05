from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.services.table.dto import TableDTO
from src.application.services.table.table import Table

from src.infra.database.repositories.income_invoice.reader import (
    Reader as InvoiceReader,
)
from src.infra.database.repositories.box.reader import Reader as BoxReader
from src.infra.database.repositories.flower_in_box.reader import Reader as FlowerReader

from src.presentation.routers.dependencies import get_session

table = APIRouter(prefix="/table", tags=["table", "services"])


@table.get(
    path="/",
    responses={status.HTTP_200_OK: {"model": TableDTO}},
)
async def get_table(
    visible: bool,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    invoice_reader = InvoiceReader(session)
    box_reader = BoxReader(session)
    flower_reader = FlowerReader(session)

    return await Table(
        invoice_reader=invoice_reader,
        box_reader=box_reader,
        flower_in_box_reader=flower_reader,
    ).get_table(visible)
