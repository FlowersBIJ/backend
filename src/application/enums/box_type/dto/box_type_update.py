from pydantic import Field

from src.application.common.dto import DTOUpdate


class BoxTypeUpdate(DTOUpdate):
    typename: str = Field(serialization_alias="label")
