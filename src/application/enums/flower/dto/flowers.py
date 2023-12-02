from src.application.common.dto import DataTransferObject
from src.application.enums.flower.dto.flower import Flower
from src.application.enums.flower.dto.flower_create import FlowerCreate
from src.application.enums.flower.dto.flower_update import FlowerUpdate

FlowerDTO = Flower | FlowerCreate | FlowerUpdate


class Flowers(DataTransferObject):
    flowers: list[Flower]
    total: int | None = None
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
