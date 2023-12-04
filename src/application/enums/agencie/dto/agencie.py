from pydantic import ConfigDict, Field

from src.application.common.dto import DataTransferObject


class Agencie(DataTransferObject):
    agencie_name: str = Field(serialization_alias="name")
    visible: bool

    model_config = ConfigDict(from_attributes=True)
