from src.application.common.dto import DTOCreate


class FlowerSortCreate(DTOCreate):
    flower_name: str
    flower_sort: str
    visible: bool
    