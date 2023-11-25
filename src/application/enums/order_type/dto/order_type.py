from src.application.common.dto import DataTransferObject


class OrderType(DataTransferObject):
    type: str
    visible: bool
    