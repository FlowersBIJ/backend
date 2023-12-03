from src.application.common.dto import DataTransferObject
from src.application.enums.flower_sort.dto.flower_sort import FlowerSort
from src.application.enums.flower_sort.dto.flower_sort_create import FlowerSortCreate
from src.application.enums.flower_sort.dto.flower_sort_update import FlowerSortUpdate

FlowerSortDTO = FlowerSort | FlowerSortCreate | FlowerSortUpdate


class FlowersSorts(DataTransferObject):
    flowers_sorts: list[FlowerSort]
    total: int | None = None
    offset: int | None = None
    limit: int | None = None
    visible: bool | None = None
