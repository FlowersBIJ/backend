from src.application.common.dto import DTOCreate


class SchemeCreate(DTOCreate):
    name: str
    description: str
