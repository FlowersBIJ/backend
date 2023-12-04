import json
from typing import Annotated

from fastapi import APIRouter, Depends, Cookie
from starlette import status
from starlette.responses import Response

from src.infra.casdoor.auth import JWTValidatorService
from src.infra.casdoor.exceptions import WrongAuthCode
from src.presentation.routers.dependencies import oauth_service_scope

auth = APIRouter(prefix="/auth", tags=["auth"])


# TODO: Сделать обычную авторизацию
@auth.post("/signin")
async def signin(code: str, response: Response,
                 oauth_service: Annotated[JWTValidatorService, Depends(oauth_service_scope)]):
    signin_data = await oauth_service.signin(code)
    response.set_cookie(key="auth_data", value=json.dumps(signin_data), httponly=True)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@auth.post("/refresh")
async def refresh(response: Response, auth_data: Annotated[str | None, Cookie()],
                  oauth_service: Annotated[JWTValidatorService, Depends(oauth_service_scope)]):
    try:
        data = json.loads(auth_data)
        data['access_token'] = await oauth_service.refresh_token(data["refresh_token"])
        response.set_cookie(key="auth_data", value=json.dumps(data))
        return response
    except json.JSONDecodeError:
        raise WrongAuthCode


@auth.post('/signout')
async def signout(oauth_service: Annotated[JWTValidatorService, Depends(oauth_service_scope)]):
    pass
