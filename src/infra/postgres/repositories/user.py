from adaptix import Retort
from psycopg import AsyncConnection

from src.infra.postgres.models.user import UserModel
from src.infra.postgres.repositories.base import BaseRepository


class UserRepository:
    _repository: BaseRepository[UserModel]

    def __init__(self, retort: Retort, connection: AsyncConnection):
        self._repository = BaseRepository(retort, connection)

    async def find_by_name(self, name: str) -> UserModel | None:
        return await (await self._repository.connection.execute(
            "SELECT * FROM user WHERE name = %s LIMIT 1", (name,)
        )).fetchone()

