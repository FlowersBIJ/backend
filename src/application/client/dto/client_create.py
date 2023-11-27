from src.application.common.dto import DTOCreate


class ClientCreate(DTOCreate):
    client_name: str
    alternative_name: str
    
    visible: bool
    
    country: str
    city: str
    
    agencie: str
    truck: str