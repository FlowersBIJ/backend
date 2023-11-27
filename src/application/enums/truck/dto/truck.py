from src.application.common.dto import DataTransferObject


class Truck(DataTransferObject):
    truck_name: str
    visible: bool
    