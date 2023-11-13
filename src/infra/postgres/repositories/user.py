from dataclasses import fields, is_dataclass

from adaptix import Retort
from psycopg import AsyncConnection

from src.infra.postgres.models.user import UserModel
from src.infra.postgres.repositories.base import BaseRepository, T


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, retort: Retort, connection: AsyncConnection):
        super().__init__(retort, connection)

    async def find_by_name(self, name: str) -> UserModel | None:
        assert is_dataclass(self.Model)

        query = (
                "SELECT " +
                ", ".join(field.name for field in fields(self.Model)) +
                " FROM %s WHERE name = %s"
        )
        return await (await self.connection.execute(
            query=query,
            params=(self.Model.table_name, name)
        )).fetchone()

    async def create_user(self, item: T) -> None:
        item_fields = fields(item)

        query = "INSERT INTO %s ("
        query += ", ".join([field.name for field in item_fields[1:]])
        query += ") VALUES ("
        query += ", ".join(["%s" for _ in range(len(item_fields) - 1)]) + ")"

        params = self.retort.dump(item)
        await self.connection.execute(
            query=query,
            params=params)

    async def update_user(self, item: T) -> None:
        pass

    async def delete_user(self, item: T) -> None:
        pass
