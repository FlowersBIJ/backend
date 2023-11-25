from src.application.common.dto import DataTransferObject


class Flower(DataTransferObject):
    name: str
    visible: bool
    