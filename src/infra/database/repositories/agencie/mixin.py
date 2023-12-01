from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.agencie.mutator import Mutator
from src.infra.database.repositories.agencie.reader import Reader


class Mixin:
    mutator: Mutator
    reader: Reader

    def __init__(self, db: AsyncSession):
        self.mutator = Mutator(db)
        self.reader = Reader(db)
