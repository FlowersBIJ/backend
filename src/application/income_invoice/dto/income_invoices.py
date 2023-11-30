from src.application.common.dto import DataTransferObject
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.income_invoice.dto.income_invoice_create import IncomeInvoiceCreate
from src.application.income_invoice.dto.income_invoice_update import IncomeInvoiceUpdate


IncomeInvoiceDTO = IncomeInvoice | IncomeInvoiceCreate | IncomeInvoiceUpdate


class IncomeInvoices(DataTransferObject):
    invoices: list[IncomeInvoiceDTO]
    total: int
    offset: int | None = None
    limit: int | None = None