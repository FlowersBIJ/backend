from src.application.common.dto import DataTransferObject
from src.application.client.dto.client import Client
from src.application.client.dto.client_create import ClientCreate
from src.application.client.dto.client_update import ClientUpdate

ClientDTO = Client | ClientCreate | ClientUpdate


class Clients(DataTransferObject):
    clients: list[ClientDTO]
    total: int
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
