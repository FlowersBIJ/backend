from pydantic import Field

from src.application.common.dto import DTOCreate


class FlowerSortCreate(DTOCreate):
    flower_name: str = Field(serialization_alias="label")
    flower_sort: str
    visible: bool
