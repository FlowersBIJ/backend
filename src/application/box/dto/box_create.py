import uuid
from datetime import date

from pydantic import Field

from src.application.common.dto import DTOCreate


class BoxCreate(DTOCreate):
    invoice_id: uuid.UUID | None = Field(default=None)
    release_date: date | None = Field(default=None)

    box_count: int = Field(gt=0)
    visible: bool = Field(default=False, description="visible or invisible for manager")

    box_type: str = Field(description="Is necessary to set at least for one flower")

    order_id: uuid.UUID
