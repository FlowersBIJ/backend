from src.application.common.dto import DataTransferObject


class Plantation(DataTransferObject):
    name: str
    visible: bool
    