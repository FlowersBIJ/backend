from pydantic import ConfigDict, Field

from src.application.common.dto import DataTransferObject


class FlowerSort(DataTransferObject):
    flower_name: str = Field(serialization_alias="name")
    flower_sort: str
    visible: bool

    model_config = ConfigDict(from_attributes=True)
