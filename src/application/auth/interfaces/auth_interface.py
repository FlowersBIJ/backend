from abc import ABC, abstractmethod
from casdoor import AsyncCasdoorSDK


class JWTValidatorService(ABC):
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

    @abstractmethod
    async def get_parsed_jwt_token(self, code):
        raise NotImplementedError
