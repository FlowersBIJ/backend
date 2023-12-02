import uuid
from abc import ABC, abstractmethod

from src.application.common.filters.filter import Filters
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoices import IncomeInvoices


class IncomeInvoiceReader(ABC):
    @abstractmethod
    async def get_by_id(self, invoice_id: uuid.UUID) -> IncomeInvoice:
        raise NotImplementedError

    @abstractmethod
    async def get_invoices(self, filters: Filters) -> IncomeInvoices:
        raise NotImplementedError

    @abstractmethod
    async def get_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def check_exists_by_id(self, invoice_id: uuid.UUID) -> bool:
        raise NotImplementedError
