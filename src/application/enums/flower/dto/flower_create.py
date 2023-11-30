from src.application.common.dto import DTOCreate


class FlowerCreate(DTOCreate):
    flower_name: str
    visible: bool
    