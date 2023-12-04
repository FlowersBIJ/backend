from pydantic import ConfigDict, Field

from src.application.common.dto import DataTransferObject


class BoxType(DataTransferObject):
    typename: str = Field(serialization_alias="label")
    visible: bool

    model_config = ConfigDict(from_attributes=True)
