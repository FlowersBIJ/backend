from src.application.common.dto import DataTransferObject
from src.application.enums.order_type.dto.order_type import OrderType
from src.application.enums.order_type.dto.order_type_create import OrderTypeCreate
from src.application.enums.order_type.dto.order_type_update import OrderTypeUpdate


OrderTypeDTO = OrderType | OrderTypeCreate | OrderTypeUpdate

class OrderTypes(DataTransferObject):
    types: list[OrderTypeDTO]
    total: int | None = None
    offset: int | None = None
    visible: bool
    