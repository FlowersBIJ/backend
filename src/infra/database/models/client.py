from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.models.base import Base

if TYPE_CHECKING:
    from src.infra.database.models.order import Order


class Agencie(Base):
    __tablename__ = "agencies"

    agencie_name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class Truck(Base):
    __tablename__ = "trucks"

    truck_name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class Client(Base):
    __tablename__ = "clients"

    client_name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    alternative_name: Mapped[str] = mapped_column(nullable=True)

    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=True)

    agencie: Mapped[str] = mapped_column(
        ForeignKey("agencies.agencie_name"), nullable=True
    )
    truck: Mapped[str] = mapped_column(ForeignKey("trucks.truck_name"), nullable=True)
