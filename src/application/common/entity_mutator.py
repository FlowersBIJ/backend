from typing import Any

from src.application.common.dto import DataTransferObject


def mutate_entity(entity: Any, dto: DataTransferObject) -> None:
    for k, v in dto.model_dump(exclude_none=True).items():
        if hasattr(entity, k):
            setattr(entity, k, v)
