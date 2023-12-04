from pydantic import ConfigDict, Field

from src.application.common.dto import DataTransferObject


class Truck(DataTransferObject):
    truck_name: str = Field(serialization_alias="label")
    visible: bool

    model_config = ConfigDict(from_attributes=True)
