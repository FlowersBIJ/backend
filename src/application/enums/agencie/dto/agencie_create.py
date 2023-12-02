from src.application.common.dto import DTOCreate


class AgencieCreate(DTOCreate):
    agencie_name: str
    visible: bool
    