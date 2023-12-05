from pydantic import Field

from src.application.common.dto import DTOUpdate


class TruckUpdate(DTOUpdate):
    truck_name: str = Field(serialization_alias="label")
