from pydantic import Field

from src.application.common.dto import DTOCreate


class BoxTypeCreate(DTOCreate):
    typename: str = Field(serialization_alias="label")
    visible: bool
