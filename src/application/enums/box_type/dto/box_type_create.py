from src.application.common.dto import DTOCreate


class BoxTypeCreate(DTOCreate):
    type: str
    visible: bool
    