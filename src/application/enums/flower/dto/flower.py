from src.application.common.dto import DataTransferObject


class Flower(DataTransferObject):
    flower_name: str
    visible: bool
    