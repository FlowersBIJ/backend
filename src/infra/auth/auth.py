from src.application.auth.interfaces.auth_interface import IJWTValidatorService


class JWTValidatorService(IJWTValidatorService):
    async def parse_jwt(self, access_token: str):
        return self.sdk.parse_jwt_token(access_token)
