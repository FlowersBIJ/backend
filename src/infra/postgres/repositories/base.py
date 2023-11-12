from dataclasses import dataclass
from typing import Generic, TypeVar, Type, Sequence

from adaptix import Retort
from psycopg import AsyncConnection

from src.infra.postgres.types import retort_row

T = TypeVar("T", contravariant=True)


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
        pass

    async def create(self, item: T) -> None:
        pass

    async def update(self, item: T) -> None:
        pass

    async def delete(self, item: T) -> None:
        pass
