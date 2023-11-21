from pydantic import BaseModel


class DataTransferObject(BaseModel):
    pass


class DTOCreate(DataTransferObject):
    pass


class DTOUpdate(DataTransferObject):
    pass
