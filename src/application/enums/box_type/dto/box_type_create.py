from src.application.common.dto import DTOCreate


class BoxTypeCreate(DTOCreate):
    typename: str
    visible: bool
    