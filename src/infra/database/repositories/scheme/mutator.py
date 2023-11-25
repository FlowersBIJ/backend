from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.entity_mutator import mutate_entity
from src.application.scheme.dto.scheme import Scheme
from src.application.scheme.dto.scheme_create import SchemeCreate
from src.application.scheme.dto.scheme_update import SchemeUpdate
from src.application.scheme.interfaces.scheme_mutator import SchemeMutator
from src.infra.database.models.models import Scheme as SchemeDB
from src.infra.database.repositories.base import BaseRepo
from src.infra.database.repositories.exceptions import (
    EntityCreateException,
    EntityDeleteException,
    EntityNotFoundException,
    EntityUpdateException,
)


class Mutator(BaseRepo, SchemeMutator):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def add(self, scheme: SchemeCreate) -> Scheme:
        new_scheme = SchemeDB()
        mutate_entity(new_scheme, scheme)

        try:
            self.db.add(new_scheme)
            await self.db.flush()
            await self.db.refresh(new_scheme)

            scheme_dto = Scheme.model_validate(new_scheme)
            return scheme_dto
        except IntegrityError:
            await self.db.rollback()
            raise EntityCreateException(scheme)

    async def update(self, scheme_id: UUID, scheme: SchemeUpdate) -> Scheme:
        scheme_db = await self.db.get(SchemeDB, scheme_id)

        if scheme_db is None:
            raise EntityNotFoundException(str(scheme_id), "Scheme")

        mutate_entity(scheme_db, scheme)

        try:
            await self.db.flush()
            await self.db.refresh(scheme_db)

            scheme_dto = Scheme.model_validate(scheme_db)
            return scheme_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityUpdateException(scheme)

    async def delete(self, scheme_id: UUID) -> Scheme:
        scheme_db = await self.db.get(SchemeDB, scheme_id)

        if scheme_db is None:
            raise EntityNotFoundException(str(scheme_id), "Scheme")

        scheme_db.deleted = True
        try:
            await self.db.flush()
            await self.db.refresh(scheme_db)

            scheme_dto = Scheme.model_validate(scheme_db)
            return scheme_dto

        except IntegrityError:
            await self.db.rollback()
            raise EntityDeleteException(str(scheme_id), "Scheme")

    async def commit(self) -> None:
        await self.db.commit()
