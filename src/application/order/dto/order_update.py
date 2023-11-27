from typing import Any
from pydantic import Field

from src.application.common.dto import DTOUpdate


class OrderUpdate(DTOUpdate):
    manager_name: str | None = Field(default=None)
    comment: str | None = Field(default=None)
    
    outcome_invoice: str | None = Field(default=None)
    
    visible: bool | None = Field(default=None)
    
    order_type: str | None = Field(default=None)
    client_name: str | None = Field(default=None)
    
    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ("manager_name", "comment", "outcome_invoice", "visible", "order_type", "client_name")
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
