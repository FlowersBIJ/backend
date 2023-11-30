from src.application.common.dto import DataTransferObject


class Agencie(DataTransferObject):
    agencie_name: str
    visible: bool
    