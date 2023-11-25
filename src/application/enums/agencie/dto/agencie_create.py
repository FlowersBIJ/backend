from src.application.common.dto import DTOCreate


class AgencieCreate(DTOCreate):
    name: str
    visible: bool
    