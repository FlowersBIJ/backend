import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.models.base import Base

if TYPE_CHECKING:
    from src.infra.database.models.client import Client
    from src.infra.database.models.box import Box


class OrderType(Base):
    __tablename__ = "order_types"

    typename: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    manager_name: Mapped[str] = mapped_column(
        nullable=False
    )  # TODO: Maybe create FK to manager from casdoor

    comment: Mapped[str] = mapped_column(nullable=True)
    outcome_invoice: Mapped[str] = mapped_column(nullable=True)

    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    order_type: Mapped[str] = mapped_column(
        ForeignKey("order_types.typename"), nullable=False
    )
    client_name: Mapped[str] = mapped_column(
        ForeignKey("clients.client_name"), nullable=False
    )
