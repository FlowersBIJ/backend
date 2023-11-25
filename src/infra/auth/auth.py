from casdoor import User

from src.application.auth.auth import IAuth
from src.application.auth.exceptions import WrongAuthCode, WrongCredentials, BaseAuthError


class CasdoorAuth(IAuth):
    async def get_oauth_token(
            self,
            code: str | None = None,
            username: str | None = None,
            password: str | None = None,
    ) -> dict:
        if code:
            try:
                return await self.sdk.get_oauth_token(code=code)
            except ValueError:
                raise WrongAuthCode
        elif username and password:
            try:
                return await self.sdk.get_oauth_token(
                    username=username, password=password
                )
            except ValueError:
                raise WrongCredentials
        else:
            raise BaseAuthError

    async def parse_jwt_token(self, token: str) -> dict:
        try:
            return self.sdk.parse_jwt_token(token)
        except Exception:
            raise BaseAuthError

    async def add_user(self, user: User) -> dict:
        try:
            return await self.sdk.add_user(user)
        except Exception:
            raise BaseAuthError

    async def delete_user(self, user: User) -> None:
        try:
            return await self.delete_user(user)
        except Exception:
            raise BaseAuthError

    async def update_user(self, user: User) -> dict:
        try:
            return await self.sdk.update_user(user)
        except Exception:
            raise BaseAuthError

    async def read_user(self, user_id: str) -> dict:
        try:
            return await self.sdk.get_user(user_id)
        except Exception:
            raise BaseAuthError

    async def read_users(self) -> dict:
        try:
            return await self.sdk.get_users()
        except Exception:
            raise BaseAuthError

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

    async def get_auth_link(
            self, redirect_uri: str, response_type: str = "code", scope: str = "read"
    ) -> str:
        try:
            return await self.sdk.get_auth_link(redirect_uri, response_type, scope)
        except Exception:
            raise BaseAuthError

    async def oauth_token_request(
            self,
            code: str | None = None,
            username: str | None = None,
            password: str | None = None,
    ) -> dict:
        if code:
            try:
                return await self.sdk.oauth_token_request(code=code)
            except ValueError:
                raise WrongAuthCode
        elif username and password:
            try:
                return await self.sdk.oauth_token_request(
                    username=username, password=password
                )
            except ValueError:
                raise WrongCredentials
        else:
            raise BaseAuthError

    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        try:
            return await self.sdk.refresh_oauth_token(refresh_token, scope)
        except Exception:
            raise BaseAuthError

    async def refresh_token_request(self, refresh_token: str, scope: str = "") -> dict:
        try:
            return await self.sdk.refresh_token_request(refresh_token, scope)
        except Exception:
            raise BaseAuthError
