import uuid
from datetime import date

from pydantic import Field

from src.application.common.dto import DTOCreate


class FlowerInBoxCreate(DTOCreate):
    income_price: float = Field(gt=0)
    outcome_price: float | None = Field(gt=0)
    hotline_miami_price: float | None = Field(gt=0)
    stems: int = Field(gt=0)

    visible: bool = Field(default=True)

    box_id: uuid.UUID
    flower_name: str
    flower_sort: str
    flower_length: str
