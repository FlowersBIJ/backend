from pydantic import Field

from src.application.common.dto import DTOUpdate


class FlowerLengthUpdate(DTOUpdate):
    flower_name: str = Field(serialization_alias="label")
    flower_sort: str
    flower_length: str
