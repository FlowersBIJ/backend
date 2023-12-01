from abc import ABC, abstractmethod

from casdoor import AsyncCasdoorSDK, User


class UIAuth(ABC):
    def __init__(self, sdk: AsyncCasdoorSDK):
        self.sdk = sdk

    @abstractmethod
    async def get_auth_link(self, redirect_uri: str, response_type: str = "code", scope: str = "read"):
        raise NotImplementedError

    @abstractmethod
    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        raise NotImplementedError

    @abstractmethod
    async def batch_enforce(
            self, permission_model_name: str, permission_rules: list[list[str]]
    ):
        raise NotImplementedError

    @abstractmethod
    async def enforce(
            self,
            permission_model_name: str,
            sub: str,
            obj: str,
            act: str,
            v3: str | None = None,
            v4: str | None = None,
            v5: str | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: User):
        return self.sdk.add_user(user)

    @abstractmethod
    async def update_user(self, user: User):
        return self.sdk.update_user(user)

    @abstractmethod
    async def delete_user(self, user: User):
        return self.sdk.delete_user(user)
