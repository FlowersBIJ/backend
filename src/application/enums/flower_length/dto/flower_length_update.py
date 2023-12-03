from src.application.common.dto import DTOUpdate


class FlowerLengthUpdate(DTOUpdate):
    flower_name: str
    flower_sort: str
    flower_length: str
