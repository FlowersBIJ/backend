from adaptix import Retort
from psycopg import AsyncConnection

from src.infra.postgres.models.user import UserModel
from src.infra.postgres.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, retort: Retort, connection: AsyncConnection):
        super().__init__(retort, connection)

    async def find_by_name(self, name: str) -> UserModel | None:
        return await (await self.connection.execute(
            "SELECT * FROM user WHERE name = %s LIMIT 1", (name,)
        )).fetchone()

