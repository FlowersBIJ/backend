from src.application.common.dto import DTOCreate


class PlantationCreate(DTOCreate):
    plantation_name: str
    visible: bool
    