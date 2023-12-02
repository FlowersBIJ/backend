from src.application.common.dto import DataTransferObject


class OrderType(DataTransferObject):
    typename: str
    visible: bool
    