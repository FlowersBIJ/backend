import uuid

from src.application.common.dto import DTOCreate


class IncomeInvoiceCreate(DTOCreate):
    invoice: str
    plantation: str
    