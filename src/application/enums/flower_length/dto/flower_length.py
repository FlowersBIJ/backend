from src.application.common.dto import DataTransferObject


class FlowerLength(DataTransferObject):
    flower_name: str
    flower_sort: str
    flower_length: str
    visible: bool
    