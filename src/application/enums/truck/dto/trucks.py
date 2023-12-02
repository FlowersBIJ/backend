from src.application.common.dto import DataTransferObject
from src.application.enums.truck.dto.truck import Truck
from src.application.enums.truck.dto.truck_create import TruckCreate
from src.application.enums.truck.dto.truck_update import TruckUpdate

TruckDTO = Truck | TruckCreate | TruckUpdate


class Trucks(DataTransferObject):
    trucks: list[Truck]
    total: int | None = None
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
