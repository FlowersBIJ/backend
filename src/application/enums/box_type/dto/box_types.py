from src.application.common.dto import DataTransferObject
from src.application.enums.box_type.dto.box_type import BoxType
from src.application.enums.box_type.dto.box_type_create import BoxTypeCreate
from src.application.enums.box_type.dto.box_type_update import BoxTypeUpdate

BoxTypeDTO = BoxType | BoxTypeUpdate | BoxTypeCreate


class BoxTypes(DataTransferObject):
    box_types: list[BoxTypeDTO]
    total: int
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
