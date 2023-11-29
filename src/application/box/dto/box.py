import uuid
from datetime import date

from src.application.common.dto import DataTransferObject


class Box(DataTransferObject):
    id: uuid.UUID
    
    invoice_id: uuid.UUID | None
    release_date: date | None
    
    box_count: int
    visible: bool
    
    box_type: str
    
    order_id: uuid.UUID
    