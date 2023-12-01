from pydantic import ConfigDict

from src.application.common.dto import DataTransferObject


class Truck(DataTransferObject):
    truck_name: str
    visible: bool
    
    model_config = ConfigDict(from_attributes=True)
    