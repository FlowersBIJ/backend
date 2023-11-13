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
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
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

    async def login(self):
        pass

    async def logout(self):
        pass
