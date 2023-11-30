from src.application.common.dto import DataTransferObject
from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencie_create import AgencieCreate
from src.application.enums.agencie.dto.agencie_update import AgencieUpdate

AgencieDTO = Agencie | AgencieCreate | AgencieUpdate


class Agencies(DataTransferObject):
    agencies: list[AgencieDTO]
    total: int | None = None
    offset: int | None = None
    limit: int | None = None
    visible: bool | None
    