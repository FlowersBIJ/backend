from pydantic import ConfigDict

from src.application.common.dto import DataTransferObject


class OrderType(DataTransferObject):
    typename: str
    visible: bool

    model_config = ConfigDict(from_attributes=True)
