from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.filters.filter import Filters, OrderFilter
from src.application.enums.agencie.dto.agencie import Agencie
from src.application.enums.agencie.dto.agencies import Agencies
from src.application.enums.agencie.interfaces.agencie_reader import AgencieReader
from src.infra.database.models.client import Agencie as AgencieDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, AgencieReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, agencie_name: str) -> Agencie:
        agencie_db = await self.db.get(AgencieDB, agencie_name)

        if agencie_db is None:
            raise EntityNotFoundException(agencie_name, "Agencie")

        agencie_dto = Agencie.model_validate(agencie_db)

        return agencie_dto

    async def get_agencies(self, filters: Filters) -> Agencies:
        query = select(AgencieDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(AgencieDB.agencie_name.asc())
        else:
            query = query.order_by(AgencieDB.agencie_name.desc())

        if filters.visible is not None:
            query = query.where(AgencieDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Agencie.model_validate(result) for result in results]
        return Agencies(
            agencies=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(AgencieDB)
        if visible:
            q = q.where(AgencieDB.visible == visible)
        return (
            await self.db.scalar(q)
        ) or 0

    async def check_exists_by_name(self, agencie_name: str) -> bool:
        query = select(exists(AgencieDB).where(AgencieDB.agencie_name == agencie_name))
        return bool(await self.db.scalar(query))
