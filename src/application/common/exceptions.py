class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "Application error occured!"


class UnexpectedError(ApplicationException):
    pass


class CommitError(ApplicationException):
    pass


class RollbackError(ApplicationException):
    pass


class RepoError(ApplicationException):
    pass


class MappingError(ApplicationException):
    pass
