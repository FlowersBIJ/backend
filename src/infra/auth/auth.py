from src.application.auth.interfaces.auth_interface import IJWTValidatorService


class JWTValidatorService(IJWTValidatorService):
    async def parse_jwt(self, access_token: str):
        """
        Converts the returned access_token to real data using
        jwt (JSON Web Token) algorithms.

        :param access_token: access_token
        :return: the data in dict format
        """
        return self.sdk.parse_jwt_token(token=access_token)
