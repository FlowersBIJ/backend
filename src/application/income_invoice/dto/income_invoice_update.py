from typing import Any
from pydantic import Field, model_validator

from src.application.common.dto import DTOUpdate


class IncomeInvoiceUpdate(DTOUpdate):
    invoice: str | None = Field(default=None)
    plantation: str | None = Field(default=None)
    
    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ("invoice", "plantation")
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
