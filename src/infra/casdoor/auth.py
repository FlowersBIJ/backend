import json

from casdoor import AsyncCasdoorSDK

from src.application.auth.interfaces.auth_interface import IJWTValidatorService
from src.infra.casdoor.exceptions import BaseAuthError, WrongCredentials, JWTDecodingException
from src.infra.log import log


class JWTValidatorService(IJWTValidatorService):
    def __init__(self,
                 endpoint: str,
                 client_id: str,
                 client_secret: str,
                 certificate: str,
                 org_name: str,
                 application_name: str,
                 front_endpoint: str) -> None:
        self.sdk = AsyncCasdoorSDK(
            endpoint,
            client_id,
            client_secret,
            certificate,
            org_name,
            application_name,
            front_endpoint,
        )
        self.logger = log()

    async def signin(self, code: str) -> dict:
        token = await self.sdk.get_oauth_token(code)
        self.logger.info(str(token))
        if 'error_description' not in token:
            raise BaseAuthError

        try:
            error = token.get('error', None)
            error_description = token.get('error_description', None)
            if error is not None or error_description is not None:
                raise WrongCredentials(error, error_description)
        except json.JSONDecodeError:
            raise JWTDecodingException

        return token

    async def refresh_token(self, token: str) -> str:
        return await self.sdk.refresh_oauth_token(token)
