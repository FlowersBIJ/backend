from abc import ABC, abstractmethod
from casdoor import AsyncCasdoorSDK


class BaseAuth(ABC):
    def __init__(self,
                 endpoint: str,
                 client_id: str,
                 client_secret: str,
                 certificate: str,
                 org_name: str,
                 application_name: str,
                 front_endpoint: str = None) -> None:
        params = {
            "endpoint": endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "certificate": certificate,
            "org_name": org_name,
            "application_name": application_name,
        }
        if front_endpoint:
            params["front_endpoint"] = front_endpoint
        self.sdk = AsyncCasdoorSDK(**params)


class IAuth(BaseAuth):
    @abstractmethod
    async def get_parsed_jwt_token(self, code):
        raise NotImplementedError

    @abstractmethod
    async def get_auth_link(self, redirect_uri: str, response_type: str = "code", scope: str = "read"):
        raise NotImplementedError

    @abstractmethod
    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        raise NotImplementedError


class UserInterface(BaseAuth):
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
