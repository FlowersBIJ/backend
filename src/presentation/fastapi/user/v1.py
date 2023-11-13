from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from src.infra.postgres.repositories.base import Filter
from src.infra.postgres.repositories.user import UserRepository
from src.presentation.fastapi.dependencies import user_repo_scope
from src.presentation.fastapi.user.scheme import GetAllUsers, GetUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/', responses={
    status.HTTP_200_OK: {
        "model": GetAllUsers
    },
})
async def get_all_users(limit: int, offset: int,
                        user_repo: Annotated[UserRepository, Depends(user_repo_scope)]) -> GetAllUsers:
    users = await user_repo.get_all(query_filter=Filter(limit=limit, offset=offset))
    return GetAllUsers(users=[GetUser.model_validate(user) for user in users], limit=limit, offset=offset)
