from src.application.common.dto import DataTransferObject
from src.application.box.dto.box import Box
from src.application.box.dto.box_create import BoxCreate
from src.application.box.dto.box_update import BoxUpdate

BoxDTO = Box | BoxCreate | BoxUpdate


class Boxes(DataTransferObject):
    boxes: list[Box]
    total: int
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
