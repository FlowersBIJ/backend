from src.application.common.dto import DTOCreate


class TruckCreate(DTOCreate):
    name: str
    visible: bool
    