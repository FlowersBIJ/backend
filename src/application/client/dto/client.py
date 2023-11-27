from src.application.common.dto import DataTransferObject


class Client(DataTransferObject):
    client_name: str
    alternative_name: str
    
    visible: bool
    
    country: str
    city: str
    
    agencie: str
    truck: str