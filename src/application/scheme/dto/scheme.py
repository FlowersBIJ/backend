from uuid import UUID

from pydantic import ConfigDict, Field

from src.application.common.dto import DataTransferObject


class Scheme(DataTransferObject):
    id: UUID

    name: str
    description: str

    deleted: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)
