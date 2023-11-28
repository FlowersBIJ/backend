import uuid
from datetime import date

from pydantic import Field

from src.application.common.dto import DataTransferObject


class Box(DataTransferObject):
    id: uuid.UUID
    
    income_invoice: str | None = Field(default=None)
    release_date: date | None = Field(default=None)
    
    box_count: int = Field(gt=0)
    visible: bool = Field(default=False, description="visible or invisible for manager")
    
    box_type: str = Field(description="Is necessary to set at least for one flower")
    plantation: str = Field()
    
    order_id: uuid.UUID
    