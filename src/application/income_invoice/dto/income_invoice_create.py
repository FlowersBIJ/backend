import uuid

from pydantic import Field

from src.application.common.dto import DTOCreate


class IncomeInvoiceCreate(DTOCreate):
    invoice: str
    plantation: str

    visible: bool = Field(default=True)
