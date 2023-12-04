from pydantic import Field

from src.application.common.dto import DTOCreate


class AgencieCreate(DTOCreate):
    agencie_name: str = Field(serialization_alias="label")
    visible: bool
