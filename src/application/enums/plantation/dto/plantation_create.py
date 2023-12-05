from pydantic import Field

from src.application.common.dto import DTOCreate


class PlantationCreate(DTOCreate):
    label: str = Field(serialization_alias="label")
    visible: bool
