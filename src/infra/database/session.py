from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable, cast

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def setup_database(
    dsn: str,
) -> tuple[Callable[[], AsyncContextManager[AsyncSession]], AsyncEngine]:
    engine = create_async_engine(
        cast(str, dsn),
        pool_pre_ping=True,
    )

    session_local = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    return session_local, engine
