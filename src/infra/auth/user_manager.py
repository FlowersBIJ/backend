from casdoor import User

from src.application.auth.repos.user_repo import UIAuth


class CasdoorUser(UIAuth):
    async def get_auth_link(
            self, redirect_uri: str, response_type: str = "code", scope: str = "read"
    ) -> str:
        return await self.sdk.get_auth_link(redirect_uri, response_type, scope)

    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        return await self.sdk.refresh_oauth_token(refresh_token, scope)

    async def batch_enforce(
            self, permission_model_name: str, permission_rules: list[list[str]]
    ) -> list[bool]:
        return await self.sdk.batch_enforce(permission_model_name, permission_rules)

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
        return await self.sdk.enforce(
            permission_model_name, sub, obj, act, v3, v4, v5
        )

    async def add_user(self, user: User):
        return self.sdk.add_user(user)

    async def update_user(self, user: User):
        return self.sdk.update_user(user)

    async def delete_user(self, user: User):
        return self.sdk.delete_user(user)
