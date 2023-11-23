from src.application.common.exceptions import ApplicationException


class DisposeException(ApplicationException):
    @property
    def message(self) -> str:
        return "Error during application disposal"


class StartServerException(ApplicationException):
    @property
    def message(self) -> str:
        return "HTTP server failed to start"
