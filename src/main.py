from adaptix import Retort, name_mapping

from src.infra.postgres.models.user import UserModel

retort = Retort(
    recipe=[
        name_mapping(
            UserModel,
            skip=["table_name"]
        )
    ]
)

print(retort.get_loader(UserModel))
