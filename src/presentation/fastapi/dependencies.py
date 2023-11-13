from starlette.requests import Request

from src.infra.postgres.repositories.user import UserRepository


async def user_repo_scope(request: Request) -> UserRepository:
    async with request.app.state.pool().connection() as connection:
        async with UserRepository(retort=request.app.state.user_retort(), connection=connection) as repo:
            yield repo
