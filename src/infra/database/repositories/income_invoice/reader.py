import uuid

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoices import IncomeInvoices
from src.application.income_invoice.interfaces.income_invoice_reader import (
    IncomeInvoiceReader,
)
from src.infra.database.models.box import IncomeInvoice as IncomeInvoiceDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, IncomeInvoiceReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_id(self, invoice_id: uuid.UUID) -> IncomeInvoice:
        income_invoice_db = await self.db.get(IncomeInvoiceDB, invoice_id)

        if income_invoice_db is None:
            raise EntityNotFoundException(str(invoice_id), "IncomeInvoice")

        income_invoice_dto = IncomeInvoice.model_validate(income_invoice_db)

        return income_invoice_dto

    async def get_invoices(self, filters: Filters) -> IncomeInvoices:
        query = select(IncomeInvoiceDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(IncomeInvoiceDB.id.asc())
        else:
            query = query.order_by(IncomeInvoiceDB.id.desc())

        # if filters.visible is not None:
        #     query = query.where(IncomeInvoiceDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count()
        dto_list = [IncomeInvoice.model_validate(result) for result in results]
        return IncomeInvoices(
            invoices=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
        )

    async def get_count(self) -> int:
        q = select(func.count()).select_from(IncomeInvoiceDB)
        return (await self.db.scalar(q)) or 0

    async def check_exists_by_id(self, invoice_id: uuid.UUID) -> bool:
        query = select(exists(IncomeInvoiceDB).where(IncomeInvoiceDB.id == invoice_id))
        return bool(await self.db.scalar(query))
