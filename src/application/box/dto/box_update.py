import uuid
from datetime import date
from typing import Any
from pydantic import Field

from src.application.common.dto import DTOUpdate


class BoxUpdate(DTOUpdate):
    income_invoice: str | None = Field(default=None)
    release_date: date | None  = Field(default=None)
    
    box_count: int | None  = Field(default=None)
    visible: bool | None  = Field(default=None)
    
    box_type: str | None  = Field(default=None)
    plantation: str | None  = Field(default=None)
    
    order_id: uuid.UUID | None  = Field(default=None)
    
    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ("income_invoice", "release_date", "box_count", "visible", "box_type", "plantation", "order_id")
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
