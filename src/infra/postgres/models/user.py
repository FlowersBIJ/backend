from dataclasses import dataclass

from src.infra.postgres.models.base import BaseModel


@dataclass(slots=True, kw_only=True)
class UserModel(BaseModel):
    table_name: str = "users"

    id: str
    username: str
    hashed_password: str
