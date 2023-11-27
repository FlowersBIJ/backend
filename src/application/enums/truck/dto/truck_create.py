from src.application.common.dto import DTOCreate


class TruckCreate(DTOCreate):
    truck_name: str
    visible: bool
    