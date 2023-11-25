from uuid import UUID

from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.schemes import Schemes
from src.application.scheme.interfaces.scheme_reader import SchemeReader
from src.infra.database.models.models import Scheme as SchemeDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import EntityNotFoundException


class Reader(BaseRepo, SchemeReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_id(self, scheme_id: UUID) -> Scheme:
        scheme_db = await self.db.get(SchemeDB, scheme_id)

        if scheme_db is None:
            raise EntityNotFoundException(str(scheme_id), "Scheme")

        scheme_dto = Scheme.model_validate(scheme_db)

        return scheme_dto

    async def get_by_name(self, filename: str) -> Scheme:
        scheme_db = await self.db.scalar(
            select(SchemeDB).where(SchemeDB.name == filename)
        )

        if scheme_db is None:
            raise EntityNotFoundException(filename, "Scheme")

        scheme_dto = Scheme.model_validate(scheme_db)

        return scheme_dto

    async def get_schemes(self, filters: Filters) -> Schemes:
        # Maybe we should implement it on BaseRepo level
        query = select(SchemeDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(SchemeDB.id.asc())
        else:
            query = query.order_by(SchemeDB.id.desc())

        if filters.deleted is not None:
            query = query.where(SchemeDB.deleted == filters.deleted)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        dto_list = [Scheme.model_validate(result) for result in results]
        return Schemes(
            schemes=dto_list,
            total=len(dto_list),
            offset=filters.offset,
            limit=filters.limit,
        )

    async def get_count(self, deleted: bool = False) -> int:
        return (
            await self.db.scalar(
                select(func.count())
                .select_from(SchemeDB)
                .where(SchemeDB.deleted == deleted)
            )
        ) or 0

    async def check_exists_by_id(self, scheme_id: UUID) -> bool:
        query = select(exists(SchemeDB).where(SchemeDB.id == scheme_id))
        return bool(await self.db.scalar(query))

    async def check_exists_by_name(self, name: str) -> bool:
        query = select(exists(SchemeDB).where(SchemeDB.name == name))
        return bool(await self.db.scalar(query))
