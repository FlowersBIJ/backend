from pydantic import Field

from src.application.common.dto import DTOUpdate


class AgencieUpdate(DTOUpdate):
    agencie_name: str = Field(serialization_alias="label")
