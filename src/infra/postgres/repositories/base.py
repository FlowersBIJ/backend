from dataclasses import dataclass, fields, is_dataclass
from typing import Generic, TypeVar, Type, Sequence

from adaptix import Retort
from psycopg import AsyncConnection

from src.infra.postgres.types import retort_row
from src.infra.postgres.models.base import BaseModel

T = TypeVar("T", contravariant=True, bound=BaseModel)


@dataclass
class Filter:
    offset: int
    limit: int


class BaseRepository(Generic[T]):
    Model: Type[T]

    def __init__(self, retort: Retort, connection: AsyncConnection):
        self.connection = connection
        self.connection.row_factory = retort_row(self.Model, retort)

    async def get_all(self, query_filter: Filter) -> Sequence[T]:
        async with self.connection as conn:
            assert is_dataclass(self.Model)
            return await (await conn.execute(
                query=f"SELECT * FROM %s OFFSET %s LIMIT %s",
                params=(self.Model.table_name, query_filter.offset, query_filter.limit)
            )).fetchall()

    async def create(self, item: T) -> None:
        async with self.connection as conn:
            item_fields = fields(item)

            query = "INSERT INTO %s ("
            query += ", ".join([field.name for field in item_fields[1:]])
            query += ") VALUES ("
            query += ", ".join(["%s" for _ in range(len(item_fields) - 1)]) + ")"

            params = tuple(getattr(item, field.name) for field in item_fields)
            await conn.execute(
                query=query,
                params=params)
            await conn.commit()

    async def update(self, item: T) -> None:
        async with (self.connection as conn):
            item_fields = tuple(getattr(item, field.name) for field in fields(item))
            table_name, _id, *other_data = item_fields

            query = "UPDATE %s SET "
            query += ", ".join([f"{field_name} = %s" for field_name in fields(item)[2:]])
            query += " WHERE id = %s"

            params = [table_name] + list(other_data)
            params.append(_id)

            await conn.execute(
                query=query,
                params=params
            )

    async def delete(self, item: T) -> None:
        async with self.connection as conn:
            query = "DELETE FROM %s WHERE id = %s"
            await conn.execute(
                query=query,
                params=tuple(getattr(item, field.name) for field in fields(item))
            )
