from src.application.common.dto import DTOCreate


class OrderCreate(DTOCreate):
    manager_name: str
    comment: str | None

    outcome_invoice: str | None

    visible: bool

    order_type: str
    client_name: str
