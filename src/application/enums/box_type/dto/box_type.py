from src.application.common.dto import DataTransferObject


class BoxType(DataTransferObject):
    type: str
    visible: bool
    