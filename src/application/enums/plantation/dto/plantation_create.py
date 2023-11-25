from src.application.common.dto import DTOCreate


class PlantationCreate(DTOCreate):
    name: str
    visible: bool
    