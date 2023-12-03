import uuid
from datetime import date

from pydantic import Field, ConfigDict

from src.application.common.dto import DataTransferObject


class FlowerInBox(DataTransferObject):
    id: uuid.UUID

    income_price: float = Field(gt=0)
    outcome_price: float | None = Field(gt=0)
    hotline_miami_price: float | None = Field(gt=0)

    stems: int

    visible: bool

    box_id: uuid.UUID
    flower_name: str
    flower_sort: str
    flower_length: str

    model_config = ConfigDict(from_attributes=True)
