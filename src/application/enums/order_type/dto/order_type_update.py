from pydantic import Field

from src.application.common.dto import DTOUpdate


class OrderTypeUpdate(DTOUpdate):
    typename: str = Field(serialization_alias="label")
