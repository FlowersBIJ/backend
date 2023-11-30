from casdoor import User

from src.application.auth.interface import IAuth, UserInterface
from src.infra.auth.exceptions import BaseAuthError, WrongAuthCode, WrongCredentials


class CasdoorAuth(IAuth):
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

    async def get_auth_link(
            self, redirect_uri: str, response_type: str = "code", scope: str = "read"
    ) -> str:
        try:
            return await self.sdk.get_auth_link(redirect_uri, response_type, scope)
        except Exception:
            raise BaseAuthError

    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        try:
            return await self.sdk.refresh_oauth_token(refresh_token, scope)
        except Exception:
            raise BaseAuthError


class CasdoorUser(UserInterface):
    async def batch_enforce(
            self, permission_model_name: str, permission_rules: list[list[str]]
    ) -> list[bool]:
        try:
            return await self.sdk.batch_enforce(permission_model_name, permission_rules)
        except Exception:
            raise BaseAuthError

    async def enforce(
            self,
            permission_model_name: str,
            sub: str,
            obj: str,
            act: str,
            v3: str | None = None,
            v4: str | None = None,
            v5: str | None = None,
    ) -> bool:
        try:
            return await self.sdk.enforce(
                permission_model_name, sub, obj, act, v3, v4, v5
            )
        except Exception:
            raise BaseAuthError

    async def add_user(self, user: User):
        return self.sdk.add_user(user)

    async def update_user(self, user: User):
        return self.sdk.update_user(user)

    async def delete_user(self, user: User):
        return self.sdk.delete_user(user)
