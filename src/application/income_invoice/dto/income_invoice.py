import uuid

from src.application.common.dto import DataTransferObject


class IncomeInvoice(DataTransferObject):
    id: uuid.UUID
    
    invoice: str
    plantation: str
    