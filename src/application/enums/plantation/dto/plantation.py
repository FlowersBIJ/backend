from src.application.common.dto import DataTransferObject


class Plantation(DataTransferObject):
    plantation_name: str
    visible: bool
    