import uuid

from pydantic import ConfigDict

from src.application.common.dto import DataTransferObject


class IncomeInvoice(DataTransferObject):
    id: uuid.UUID
    
    invoice: str
    plantation: str
    
    model_config = ConfigDict(from_attributes=True)
    