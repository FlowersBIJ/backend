from src.application.common.dto import DTOCreate


class FlowerSortCreate(DTOCreate):
    type_name: str
    sort_name: str
    visible: bool
    