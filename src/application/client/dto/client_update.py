from typing import Any
from pydantic import Field

from src.application.common.dto import DTOUpdate


class ClientUpdate(DTOUpdate):
    alternative_name: str | None = Field(default=None)
    
    visible: bool | None = Field(default=None)
    
    country: str | None = Field(default=None)
    city: str | None = Field(default=None) 
    
    agencie: str | None = Field(default=None)
    truck: str | None = Field(default=None)
    
    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ("alternative_name", "visible", "country", "city", "agencie", "truck")
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
    