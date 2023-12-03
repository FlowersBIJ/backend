import uuid
from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.models.base import Base

if TYPE_CHECKING:
    from src.infra.database.models.box import Box


class Flower(Base):
    __tablename__ = "flowers"

    flower_name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    # sorts: Mapped[list["FlowerSort"]] = relationship(back_populates="type")


class FlowerSort(Base):
    __tablename__ = "flower_sorts"

    flower_name: Mapped[str] = mapped_column(
        ForeignKey("flowers.flower_name"), primary_key=True
    )
    flower_sort: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class FlowerLength(Base):
    __tablename__ = "flowers_length"

    flower_name: Mapped[str] = mapped_column(primary_key=True)
    flower_sort: Mapped[str] = mapped_column(primary_key=True)
    flower_length: Mapped[str] = mapped_column(primary_key=True)

    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    __table_args__: tuple = (
        ForeignKeyConstraint(
            [flower_name, flower_sort], [FlowerSort.flower_name, FlowerSort.flower_sort]
        ),
        {},
    )


class FlowerInBox(Base):
    __tablename__ = "flowers_in_box"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ["flower_name", "flower_sort", "flower_length"],
            [
                FlowerLength.flower_name,
                FlowerLength.flower_sort,
                FlowerLength.flower_sort,
            ],
        ),
        {},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    stems: Mapped[int] = mapped_column(nullable=False)
    income_price: Mapped[float] = mapped_column(nullable=False)
    outcome_price: Mapped[float] = mapped_column(nullable=True)
    hotline_miami_price: Mapped[float] = mapped_column(nullable=True)

    visible: Mapped[bool] = mapped_column(nullable=False, default=True)

    box_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("boxes.id"), nullable=False)

    flower_name: Mapped[str] = mapped_column(nullable=False)
    flower_sort: Mapped[str] = mapped_column(nullable=False)
    flower_length: Mapped[str] = mapped_column(nullable=False)
