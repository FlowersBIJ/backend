from src.application.common.exceptions import ApplicationException


class BaseAuthError(ApplicationException):
    @property
    def message(self) -> str:
        return "Auth error occurred!"


class JWTDecodingException(BaseAuthError):
    @property
    def message(self) -> str:
        return "JWT Decoding exception"


class WrongAuthCode(BaseAuthError):
    @property
    def message(self) -> str:
        return "Wrong authorization code."


class WrongCredentials(BaseAuthError):
    def __init__(self, error: str, error_description: str) -> None:
        self.error = error
        self.error_description = error_description

    @property
    def message(self) -> str:
        return f"{self.error} - {self.error_description}"
