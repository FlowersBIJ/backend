from src.application.common.dto import DTOCreate


class OrderTypeCreate(DTOCreate):
    type: str
    visible: bool
    