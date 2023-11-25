import uuid

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class FlowerType(Base):
    __tablename__ = "flower_type"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, unique=True, default=uuid.uuid4()
    )
    type_name: Mapped[str] = mapped_column(nullable=False)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class Plantation(Base):
    __tablename__ = "plantation"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, unique=True, default=uuid.uuid4()
    )
    plantation_name: Mapped[str] = mapped_column(nullable=False)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
