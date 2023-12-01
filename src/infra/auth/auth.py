from src.application.auth.interfaces.auth_interface import IJWTValidatorService
from src.infra.auth.exceptions import BaseAuthError, WrongAuthCode, WrongCredentials


class JWTValidatorService(IJWTValidatorService):
    async def get_parsed_jwt_token(
            self,
            code: str | None = None,
            username: str | None = None,
            password: str | None = None):
        if code:
            try:
                token = await self.sdk.get_oauth_token(code=code)
                access_token = token.get("access_token")
                return self.sdk.parse_jwt_token(access_token)
            except ValueError:
                raise WrongAuthCode
        elif username and password:
            try:
                token = await self.sdk.get_oauth_token(username=username, password=password)
                access_token = token.get("access_token")
                return self.sdk.parse_jwt_token(access_token)
            except ValueError:
                raise WrongCredentials
        else:
            raise BaseAuthError
