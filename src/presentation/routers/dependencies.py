from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.requests import Request


async def get_session(request: Request):
    session_maker: async_sessionmaker = request.app.state.db_session
    async with session_maker() as s:
        yield s
