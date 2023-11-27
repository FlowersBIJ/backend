import uuid
from datetime import date

from src.application.common.dto import DataTransferObject


class FlowerInBox(DataTransferObject):
    id: uuid.UUID
    
    income_price_per_stem: float
    outcome_price_per_stem: float | None
    hotline_miami_price_per_stem: float | None
    
    visible: bool
    
    box_id: uuid.UUID
    flower_name: str
    flower_sort: str
    flower_length: str
    