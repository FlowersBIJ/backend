from pydantic import ConfigDict

from src.application.common.dto import DataTransferObject


class BoxType(DataTransferObject):
    typename: str
    visible: bool

    model_config = ConfigDict(from_attributes=True)
