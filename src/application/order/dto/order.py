import uuid

from src.application.common.dto import DataTransferObject


class Order(DataTransferObject):
    id: uuid.UUID
    
    manager_name: str
    comment: str | None
    
    outcome_invoice: str | None
    
    visible: bool
    
    order_type: str
    client_name: str