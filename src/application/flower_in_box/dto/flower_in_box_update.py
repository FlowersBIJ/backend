import uuid
from datetime import date
from typing import Any
from pydantic import Field, model_validator

from src.application.common.dto import DTOUpdate


class FlowerInBoxUpdate(DTOUpdate):
    income_price: float | None = Field(default=None, gt=0)
    outcome_price: float | None = Field(default=None, gt=0)
    hotline_miami_price: float | None = Field(default=None, gt=0)

    stems: int | None = Field(default=0, gt=0)

    visible: bool | None = Field(default=None)

    box_id: uuid.UUID | None = Field(default=None)
    flower_name: str | None = Field(default=None)
    flower_sort: str | None = Field(default=None)
    flower_length: str | None = Field(default=None)

    @model_validator(mode="before")  # type: ignore
    def check_something_exists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            fields = (
                "income_price",
                "outcome_price",
                "hotline_miami_price",
                "visible",
                "box_id",
                "flower_name",
                "flower_sort",
                "flower_length",
            )
            if all(x not in data for x in fields):
                raise ValueError
            return data
        raise ValueError
