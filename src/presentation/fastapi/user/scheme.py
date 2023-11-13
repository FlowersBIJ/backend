from pydantic import BaseModel


class GetUser(BaseModel):
    username: str
    # ...


class GetAllUsers(BaseModel):
    offset: int
    limit: int
    users: list[GetUser]
