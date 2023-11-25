from src.application.common.dto import DTOCreate


class FlowerCreate(DTOCreate):
    name: str
    visible: bool
    