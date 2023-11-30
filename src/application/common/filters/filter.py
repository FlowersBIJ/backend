from enum import Enum

from src.application.common.dto import DataTransferObject


class OrderFilter(Enum):
    ASC = "asc"
    DESC = "desc"


class Filters(DataTransferObject):
    offset: int | None = None
    limit: int | None = None
    invisible: bool | None = None
    order: OrderFilter = OrderFilter.ASC
