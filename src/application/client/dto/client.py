from pydantic import Field, ConfigDict

from src.application.common.dto import DataTransferObject


class Client(DataTransferObject):
    client_name: str
    alternative_name: str

    visible: bool = Field(default=False, description="visible or invisible for manager")

    country: str
    city: str

    agencie: str
    truck: str
    
    model_config = ConfigDict(from_attributes=True)
