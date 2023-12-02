from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.client.dto.client import Client
from src.application.client.dto.clients import Clients
from src.application.client.interfaces.client_reader import ClientReader
from src.application.common.filters.filter import Filters, OrderFilter
from src.infra.database.models.client import Client as ClientDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
)


class Reader(BaseRepo, ClientReader):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def get_by_name(self, name: str) -> Client:
        client_db = await self.db.get(ClientDB, name)

        if client_db is None:
            raise EntityNotFoundException(str(name), "Client")

        client_dto = Client.model_validate(client_db)

        return client_dto

    async def get_clients(self, filters: Filters) -> Clients:
        query = select(ClientDB)
        if filters.order is OrderFilter.ASC:
            query = query.order_by(ClientDB.client_name.asc())
        else:
            query = query.order_by(ClientDB.client_name.desc())

        if filters.visible is not None:
            query = query.where(ClientDB.visible == filters.visible)

        if filters.offset is not None:
            query = query.offset(filters.offset)

        if filters.limit is not None:
            query = query.limit(filters.limit)

        results = await self.db.scalars(query)
        total = await self.get_count(visible=filters.visible)
        dto_list = [Client.model_validate(result) for result in results]
        return Clients(
            clients=dto_list,
            total=total,
            offset=filters.offset,
            limit=filters.limit,
            visible=filters.visible
        )

    async def get_count(self, visible: bool | None = None) -> int:
        q = select(func.count()).select_from(ClientDB)
        if visible:
            q = q.where(ClientDB.visible == visible)
        return (
            await self.db.scalar(q)
        ) or 0

    async def check_exists_by_name(self, name: str) -> bool:
        query = select(exists(ClientDB).where(ClientDB.client_name == name))
        return bool(await self.db.scalar(query))
