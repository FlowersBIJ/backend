from dataclasses import dataclass

from src.infra.postgres.models.base import BaseModel


@dataclass(slots=True, kw_only=True)
class UserModel(BaseModel):
    id: str
    username: str
    hashed_password: str
