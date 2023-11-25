from src.application.common.dto import DataTransferObject
from src.application.enums.plantation.dto.plantation import Plantation
from src.application.enums.plantation.dto.plantation_create import PlantationCreate
from src.application.enums.plantation.dto.plantation_update import PlantationUpdate


PlantationDTO = Plantation | PlantationCreate | PlantationUpdate

class Plantations(DataTransferObject):
    plantations: list[PlantationDTO]
    total: int | None = None
    offset: int | None = None
    visible: bool
    