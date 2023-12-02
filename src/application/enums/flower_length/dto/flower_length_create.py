from src.application.common.dto import DTOCreate


class FlowerLengthCreate(DTOCreate):
    flower_name: str
    flower_sort: str
    flower_length: str
    visible: bool
    