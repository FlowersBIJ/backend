import uuid
from datetime import date

from src.application.common.dto import DTOCreate


class BoxCreate(DTOCreate):
    invoice_id: uuid.UUID | None
    release_date: date | None
    
    box_count: int
    visible: bool
    
    box_type: str
    
    order_id: uuid.UUID
    