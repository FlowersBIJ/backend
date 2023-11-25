import abc

from casdoor import AsyncCasdoorSDK, User


class IAuth(abc.ABC):
    def __init__(
        self,
        endpoint,
        client_id,
        client_secret,
        certificate,
        org_name,
        application_name,
    ) -> None:
        self.sdk = AsyncCasdoorSDK(
            endpoint=endpoint,
            client_id=client_id,
            client_secret=client_secret,
            certificate=certificate,
            org_name=org_name,
            application_name=application_name,
        )

    @abc.abstractmethod
    async def get_oauth_token(
        self,
        code: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        pass

    @abc.abstractmethod
    async def parse_jwt_token(self, token: str):
        pass

    @abc.abstractmethod
    async def add_user(self, user: User):
        pass

    @abc.abstractmethod
    async def delete_user(self, user: User):
        pass

    @abc.abstractmethod
    async def update_user(self, user: User):
        pass

    @abc.abstractmethod
    async def read_user(self, user_id: str):
        pass

    @abc.abstractmethod
    async def read_users(self):
        pass

    @abc.abstractmethod
    async def batch_enforce(
        self, permission_model_name: str, permission_rules: list[list[str]]
    ):
        pass

    @abc.abstractmethod
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
        pass

    @abc.abstractmethod
    async def get_auth_link(
        self, redirect_uri: str, response_type: str = "code", scope: str = "read"
    ):
        pass

    @abc.abstractmethod
    async def oauth_token_request(
        self,
        code: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> dict:
        pass

    @abc.abstractmethod
    async def refresh_oauth_token(self, refresh_token: str, scope: str = "") -> str:
        pass

    @abc.abstractmethod
    async def refresh_token_request(self, refresh_token: str, scope: str = "") -> dict:
        pass
