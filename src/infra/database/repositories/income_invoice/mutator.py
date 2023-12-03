import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoice_create import IncomeInvoiceCreate
from src.application.income_invoice.dto.income_invoice_update import IncomeInvoiceUpdate
from src.application.income_invoice.interfaces.income_invoice_mutator import (
    IncomeInvoiceMutator,
)
from src.infra.database.models.box import IncomeInvoice as IncomeInvoiceDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityNotFoundException,
    EntityDeleteException,
    EntityUpdateException,
    EntityVisibilityChangeException,
)


class Mutator(BaseRepo, IncomeInvoiceMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, invoice: IncomeInvoiceCreate) -> IncomeInvoice:
        new_income_invoice = IncomeInvoiceDB()
        mutate_entity(new_income_invoice, invoice)

        try:
            self.db.add(new_income_invoice)
            await self.db.flush()
            await self.db.refresh(new_income_invoice)

            income_invoice_dto = IncomeInvoice.model_validate(new_income_invoice)
            return income_invoice_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(invoice)

    async def delete(self, invoice_id: uuid.UUID) -> None:
        income_invoice_db = await self.db.get(IncomeInvoiceDB, invoice_id)

        if income_invoice_db is None:
            raise EntityNotFoundException(str(invoice_id), "IncomeInvoice")

        await self.db.delete(income_invoice_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(invoice_id), "IncomeInvoice")

    async def update(
        self, invoice_id: uuid.UUID, invoice: IncomeInvoiceUpdate
    ) -> IncomeInvoice:
        income_invoice_db = await self.db.get(IncomeInvoiceDB, invoice_id)

        if income_invoice_db is None:
            raise EntityNotFoundException(str(invoice_id), "Box")

        mutate_entity(income_invoice_db, invoice)

        try:
            await self.db.flush()
            await self.db.refresh(income_invoice_db)

            income_invoice_dto = IncomeInvoice.model_validate(income_invoice_db)
            return income_invoice_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(invoice)

    async def change_visibility(self, invoice_id: uuid.UUID) -> IncomeInvoice:
        invoice_db = await self.db.get(IncomeInvoiceDB, invoice_id)

        if invoice_db is None:
            raise EntityNotFoundException(str(invoice_id), "IncomveInvoice")

        invoice_db.visible = not invoice_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(invoice_db)

            invoice_dto = IncomeInvoice.model_validate(invoice_db)
            return invoice_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(str(invoice_id), "IncomeInvoice")

    async def commit(self) -> None:
        await self.db.commit()
