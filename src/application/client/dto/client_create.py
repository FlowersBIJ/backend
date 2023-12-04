from pydantic import Field, model_validator

from src.application.common.dto import DTOCreate


class ClientCreate(DTOCreate):
    client_name: str
    alternative_name: str

    visible: bool = Field(default=True, description="visible or invisible for manager")

    country: str
    city: str

    agencie: str
    truck: str

    @model_validator(mode="after")
    def validate_delivery(self) -> "ClientCreate":
        if self.agencie or self.truck:
            return self
        raise ValueError("agencie or truck must be set")