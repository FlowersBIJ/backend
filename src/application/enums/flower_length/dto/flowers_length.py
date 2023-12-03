from src.application.common.dto import DataTransferObject
from src.application.enums.flower_length.dto.flower_length import FlowerLength
from src.application.enums.flower_length.dto.flower_length_create import (
    FlowerLengthCreate,
)
from src.application.enums.flower_length.dto.flower_length_update import (
    FlowerLengthUpdate,
)

FlowerLengthDTO = FlowerLength | FlowerLengthCreate | FlowerLengthUpdate


class FlowersLength(DataTransferObject):
    flowers_length: list[FlowerLength]
    total: int | None = None
    offset: int | None = None
    limit: int | None = None
    visible: bool | None = None
