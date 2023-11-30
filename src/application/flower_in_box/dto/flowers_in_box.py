from src.application.common.dto import DataTransferObject
from src.application.flower_in_box.dto.flower_in_box import FlowerInBox
from src.application.flower_in_box.dto.flower_in_box_create import FlowerInBoxCreate
from src.application.flower_in_box.dto.flower_in_box_update import FlowerInBoxUpdate


FlowerInBoxDTO = FlowerInBox | FlowerInBoxCreate | FlowerInBoxUpdate


class FlowersInBox(DataTransferObject):
    flowers: list[FlowerInBoxDTO]
    total: int
    offset: int | None = None
    limit: int | None = None
    visible: bool | None = None
