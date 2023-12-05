from pydantic import Field

from src.application.common.dto import DTOCreate


class FlowerLengthCreate(DTOCreate):
    flower_name: str = Field(serialization_alias="label")
    flower_sort: str
    flower_length: str
    visible: bool
