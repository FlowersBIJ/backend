from src.application.common.dto import DataTransferObject


class FlowerSort(DataTransferObject):
    flower_name: str
    flower_sort: str
    visible: bool
    