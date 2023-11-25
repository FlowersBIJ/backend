from src.application.common.dto import DataTransferObject


class FlowerSort(DataTransferObject):
    type_name: str
    sort_name: str
    visible: bool
    