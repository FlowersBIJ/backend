from pydantic import Field

from src.application.common.dto import DTOUpdate


class PlantationUpdate(DTOUpdate):
    plantation_name: str = Field(serialization_alias="label")
