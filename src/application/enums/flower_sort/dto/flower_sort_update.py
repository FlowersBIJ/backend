from pydantic import Field

from src.application.common.dto import DTOUpdate


class FlowerSortUpdate(DTOUpdate):
    flower_name: str = Field(serialization_alias="label")
    flower_sort: str
