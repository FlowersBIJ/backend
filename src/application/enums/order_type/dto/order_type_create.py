from src.application.common.dto import DTOCreate


class OrderTypeCreate(DTOCreate):
    typename: str
    visible: bool
