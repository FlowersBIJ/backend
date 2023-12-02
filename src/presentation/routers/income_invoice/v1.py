import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoice_create import IncomeInvoiceCreate
from src.application.income_invoice.dto.income_invoice_update import IncomeInvoiceUpdate
from src.application.income_invoice.dto.income_invoices import IncomeInvoices
from src.application.common.filters.filter import Filters
from src.infra.database.repositories.income_invoice.mutator import Mutator
from src.infra.database.repositories.income_invoice.reader import Reader
from src.presentation.routers.dependencies import get_session

income_invoices = APIRouter(prefix="/income_invoices", tags=["income_invoices"])


@income_invoices.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": IncomeInvoice},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_income_invoice(
        income_invoice_create: IncomeInvoiceCreate, session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    created_income_invoice = await mutator.add(income_invoice_create)
    await mutator.commit()
    return created_income_invoice


@income_invoices.put(
    path="/change_visibility/{invoice_id}",
    responses={
        status.HTTP_200_OK: {"model": IncomeInvoice},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def change_visibility_income_invoice(
        invoice_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_invoice = await mutator.change_visibility(invoice_id=invoice_id)
    await mutator.commit()
    return updated_invoice


@income_invoices.delete(
    path="/delete/{invoice_id}",
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_income_invoice(
        invoice_id: uuid.UUID,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    mutator = Mutator(session)
    deleted_income_invoice = await mutator.delete(invoice_id=invoice_id)
    await mutator.commit()
    return deleted_income_invoice


@income_invoices.put(
    path="/id/{income_invoice_id}",
    responses={
        status.HTTP_200_OK: {"model": IncomeInvoice},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_income_invoice(
        invoice_id: uuid.UUID,
        income_invoice_update: IncomeInvoiceUpdate,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    mutator = Mutator(session)
    updated_scheme = await mutator.update(
        invoice_id=invoice_id,
        invoice=income_invoice_update
    )
    await mutator.commit()
    return updated_scheme


@income_invoices.get(
    path="/id/{income_invoice_id}",
    responses={
        status.HTTP_200_OK: {"model": IncomeInvoice},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_income_invoice(
        invoice_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    income_invoice = await reader.get_by_id(invoice_id=invoice_id)
    return income_invoice


@income_invoices.get(path="/count", responses={status.HTTP_200_OK: {"model": int}})
async def get_income_invoices_count(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    reader = Reader(session)
    count = await reader.get_count()
    return count


@income_invoices.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": IncomeInvoices},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_income_invoices(
        session: Annotated[AsyncSession, Depends(get_session)], filters: Filters = Depends()
):
    reader = Reader(session)
    filtered_income_invoices = await reader.get_invoices(filters=filters)
    return filtered_income_invoices


@income_invoices.get(
    path="/exists/name/{income_invoice_name}",
    responses={
        status.HTTP_200_OK: {"model": bool},
    },
)
async def income_invoice_exists_by_id(
        invoice_id: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    reader = Reader(session)
    exists = await reader.check_exists_by_id(invoice_id)
    return exists
