import uuid

from pydantic import ConfigDict

from src.application.common.dto import DataTransferObject


class Order(DataTransferObject):
    id: uuid.UUID

    manager_name: str
    comment: str | None

    outcome_invoice: str | None

    visible: bool

    order_type: str
    client_name: str

    model_config = ConfigDict(from_attributes=True)
