import uuid
from datetime import date

from pydantic import Field

from src.application.common.dto import DataTransferObject


class FlowerInBox(DataTransferObject):
    id: uuid.UUID
    
    income_price_per_stem: float = Field(gt=0)
    outcome_price_per_stem: float | None = Field(gt=0)
    hotline_miami_price_per_stem: float | None = Field(gt=0)
    
    visible: bool
    
    box_id: uuid.UUID
    flower_name: str
    flower_sort: str
    flower_length: str
    