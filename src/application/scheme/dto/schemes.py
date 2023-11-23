from src.application.common.dto import DataTransferObject
from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.scheme_create import SchemeCreate
from src.application.scheme.dto.scheme_update import SchemeUpdate


SchemeDTOs = Scheme | SchemeCreate | SchemeUpdate


class Schemes(DataTransferObject):
    schemes: list[Scheme]
    total: int
    offset: int | None = None
    limit: int | None = None
