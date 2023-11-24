from src.application.common.exceptions import ApplicationException


class BaseAuthError(ApplicationException):
    @property
    def message(self) -> str:
        return "Auth error occurred!"


class WrongAuthCode(BaseAuthError):
    @property
    def message(self) -> str:
        return "Wrong authorization code."


class WrongCredentials(BaseAuthError):
    @property
    def message(self) -> str:
        return "Wrong username or password for authorization server."
