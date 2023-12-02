from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.client.dto.client import Client
from src.application.client.dto.client_create import ClientCreate
from src.application.client.dto.client_update import ClientUpdate
from src.application.client.interfaces.client_mutator import ClientMutator
from src.application.common.entity_mutator import mutate_entity
from src.infra.database.models.client import Client as ClientDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityUpdateException,
    EntityNotFoundException,
    EntityDeleteException, EntityVisibilityChangeException,
)


class Mutator(BaseRepo, ClientMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, client: ClientCreate) -> Client:
        new_client = ClientDB()
        mutate_entity(new_client, client)

        try:
            self.db.add(new_client)
            await self.db.flush()
            await self.db.refresh(new_client)

            client_dto = Client.model_validate(new_client)
            return client_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(client)

    async def update(self, client_name: str, client: ClientUpdate) -> Client:
        client_db = await self.db.get(ClientDB, client_name)

        if client_db is None:
            raise EntityNotFoundException(str(client_name), "Client")

        mutate_entity(client_db, client)

        try:
            await self.db.flush()
            await self.db.refresh(client_db)

            client_dto = Client.model_validate(client_db)
            return client_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(client)

    async def delete(self, client_name: str) -> Client:
        client_db = await self.db.get(ClientDB, client_name)

        if client_db is None:
            raise EntityNotFoundException(str(client_name), "Client")

        await self.db.delete(client_db)
        try:
            await self.db.flush()

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(client_name), "Client")

    async def change_visibility(self, client_name: str) -> Client:
        client_db = await self.db.get(ClientDB, client_name)

        if client_db is None:
            raise EntityNotFoundException(str(client_name), "Client")

        client_db.visible = not client_db.visible

        try:
            await self.db.flush()
            await self.db.refresh(client_db)

            client_dto = Client.model_validate(client_db)
            return client_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityVisibilityChangeException(str(client_name), "Client")

    async def commit(self) -> None:
        await self.db.commit()
