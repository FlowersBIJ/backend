import uuid
from abc import ABC, abstractmethod

from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoice_create import IncomeInvoiceCreate
from src.application.income_invoice.dto.income_invoice_update import IncomeInvoiceUpdate


class IncomeInvoiceMutator(ABC):
    @abstractmethod
    async def add(self, invoice: IncomeInvoiceCreate) -> IncomeInvoice:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, invoice_id: uuid.UUID, invoice: IncomeInvoiceUpdate
    ) -> IncomeInvoice:
        raise NotImplementedError

    @abstractmethod
    async def change_visibility(self, invoice_id: uuid.UUID) -> IncomeInvoice:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, invoice_id: uuid.UUID) -> None:
        raise NotImplementedError
