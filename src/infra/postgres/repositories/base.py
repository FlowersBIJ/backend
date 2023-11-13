import logging
from dataclasses import dataclass, fields, is_dataclass
from types import TracebackType
from typing import Generic, TypeVar, Type, Sequence, Optional

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
        self.retort = retort
        self.connection = connection
        self.connection.row_factory = retort_row(self.Model, retort)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.connection.closed:
            return

        if exc_type:
            # try to rollback, but if there are problems (connection in a bad
            # state) just warn without clobbering the exception bubbling up.
            try:
                await self.connection.rollback()
            except Exception as exc2:
                self.logger.warning(
                    "error ignored in rollback on %s: %s",
                    self.connection,
                    exc2,
                )
        else:
            await self.connection.commit()

    async def get_all(self, query_filter: Filter) -> Sequence[T]:
        assert is_dataclass(self.Model)
        query = ("SELECT" +
                 ", ".join([field.name for field in fields(self.Model)]) +
                 " FROM " + self.Model.table_name + " OFFSET %s LIMIT %s")
        return await (await self.connection.execute(
            query=query,
            params=(query_filter.offset, query_filter.limit)
        )).fetchall()

    async def create(self, item: T) -> None:
        item_fields = fields(item)

        query = "INSERT INTO %s ("
        query += ", ".join([field.name for field in item_fields[1:]])
        query += ") VALUES ("
        query += ", ".join(["%s" for _ in range(len(item_fields) - 1)]) + ")"

        params = self.retort.dump(item)
        await self.connection.execute(
            query=query,
            params=params)

    async def update(self, item: T) -> None:
        item_fields = tuple(getattr(item, field.name) for field in fields(item))
        table_name, _id, *other_data = item_fields

        query = "UPDATE %s SET "
        query += ", ".join([f"{field_name} = %s" for field_name in fields(item)[2:]])
        query += " WHERE id = %s"

        params = [table_name] + list(other_data)
        params.append(_id)

        await self.connection.execute(
            query=query,
            params=params
        )

    async def delete(self, item: T) -> None:
        query = "DELETE FROM %s WHERE id = %s"
        await self.connection.execute(
            query=query,
            params=tuple(getattr(item, field.name) for field in fields(item))
        )
