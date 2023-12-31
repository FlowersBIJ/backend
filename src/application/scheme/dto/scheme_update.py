from typing import Any

from pydantic import Field, model_validator

from src.application.common.dto import DTOUpdate


class SchemeUpdate(DTOUpdate):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)

    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = ("name", "description")
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
