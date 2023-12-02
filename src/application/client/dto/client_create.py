from pydantic import Field

from src.application.common.dto import DTOCreate


class ClientCreate(DTOCreate):
    client_name: str
    alternative_name: str

    visible: bool = Field(default=True, description="visible or invisible for manager")

    country: str
    city: str

    agencie: str
    truck: str
