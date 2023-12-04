from pydantic import Field

from src.application.common.dto import DTOCreate


class TruckCreate(DTOCreate):
    truck_name: str = Field(serialization_alias="label")
    visible: bool
