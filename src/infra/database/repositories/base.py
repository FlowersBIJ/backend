from sqlalchemy.ext.asyncio import AsyncSession
from structlog.stdlib import BoundLogger

from src.infra.log import log


class BaseRepo:
    logger: BoundLogger
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.logger = log()
        self.db = db
