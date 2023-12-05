from pydantic import Field

from src.application.common.dto import DTOCreate


class FlowerCreate(DTOCreate):
    flower_name: str = Field(serialization_alias="label")
    visible: bool
