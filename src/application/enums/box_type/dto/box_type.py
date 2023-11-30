from src.application.common.dto import DataTransferObject


class BoxType(DataTransferObject):
    typename: str
    visible: bool
    