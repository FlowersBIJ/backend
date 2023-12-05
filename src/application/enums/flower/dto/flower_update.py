from pydantic import Field

from src.application.common.dto import DTOUpdate


class FlowerUpdate(DTOUpdate):
    flower_name: str = Field(serialization_alias="label")
