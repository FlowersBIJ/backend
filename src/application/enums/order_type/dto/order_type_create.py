from pydantic import Field

from src.application.common.dto import DTOCreate


class OrderTypeCreate(DTOCreate):
    typename: str = Field(serialization_alias="label")
    visible: bool
