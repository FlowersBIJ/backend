from src.application.common.dto import DataTransferObject
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_type_create import BoxTypeCreate
from src.application.enums.box_type.dto.box_type_update import BoxTypeUpdate


BoxTypeDTO = BoxType | BoxTypeUpdate | BoxTypeCreate

class BoxTypes(DataTransferObject):
    boxes: list[BoxTypeDTO]
    total: int | None = None
    offset: int | None = None
    visible: bool
    