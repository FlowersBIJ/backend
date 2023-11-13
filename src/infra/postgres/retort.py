from adaptix import Retort, name_mapping

from src.infra.postgres.models.user import UserModel


class UserRetort(Retort):
    def __init__(self):
        super().__init__(
            recipe=[
                name_mapping(
                    UserModel,
                    skip=["table_name"]
                )
            ]
        )
