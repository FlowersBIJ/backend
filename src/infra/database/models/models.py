import uuid
import datetime

from sqlalchemy import MetaData, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


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


class Order(Base):
    __tablename__ = "order"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4()
    )
    manager_name: Mapped[str] = mapped_column(
        nullable=False
    ) # TODO: Maybe create FK to manager from casdoor

    comment: Mapped[str] = mapped_column(nullable=True)
    invoice: Mapped[str] = mapped_column(nullable=False) # насколько понимаю, это номер заказа, тоже уникальный - у одного заказчика не встречается несколько раз
    # лучше вынести в отдельную сущность - (invoice + label)
    

class Client(Base):
    __tablename__ = "client"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    
    name: Mapped[str] = mapped_column(nullable=False)
    alternative_name: Mapped[str] = mapped_column(nullable=True)
    
    agencie: Mapped[str] = mapped_column(nullable=False)
    truck: Mapped[str] = mapped_column(nullable=False)
    
    country: Mapped[str] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(primary_key=True)
    
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="label") 


class ClientInvoice(Base):
    __tablename__ = "client_invoice"
    
    cleint_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())


class Box(Base):
    __tablename__ = "box"

    # выделить цветы в коробке
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4()
    )
    
    box_type: Mapped[str] = mapped_column(
        nullable=True, default=None
    )
    
    flower: Mapped[str] = mapped_column(
        nullable=False
    )
    flower_sort: Mapped[str] = mapped_column(
        nullable=False
    )
    flower_length: Mapped[str] = mapped_column(
        nullable=False
    )  # TODO: Выделить в дропдаун
    plantation: Mapped[str] = mapped_column(
        nullable=False
    )
    stems: Mapped[int] = mapped_column(
        nullable=False
    )
    income_price_per_stem: Mapped[float] = mapped_column(
        nullable=False
    )
    outcome_price_per_stem: Mapped[float] = mapped_column(
        nullable=True
    )
    hotline_miami_price_per_stem: Mapped[float] = mapped_column(
        nullable=True
    )
    count: Mapped[str] = mapped_column(
        nullable=False
    )
    
    
class Outcome(Base):
    __tablename__ = "outcome"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4()
    )
    release_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False
    ) # Дата отгрузки
    invoice: Mapped[str] = mapped_column(
        nullable=False
    ) # можем сделать первичным ключом
    awb: Mapped[str] = mapped_column(
        nullable=False
    )
    labeling: Mapped[str] = mapped_column(
        ForeignKey("label.name"), nullable=False
    )
    cargo_agencie: Mapped[str] = mapped_column(
        ForeignKey("agencie.name"), nullable=True
    )
    truck_name: Mapped[str] = mapped_column(
        ForeignKey("truck.name"), nullable=True
    )
    
    label: Mapped["Label"] = relationship(back_populates="outcomes")
    agencie: Mapped["Agencie"] = relationship(back_populates="outcomes")
    truck: Mapped["Truck"] = relationship(back_populates="outcomes")





class Flower(Base):
    __tablename__ = "flower"
    
    name: Mapped[str] = mapped_column(
        primary_key=True
    )
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    sorts: Mapped[list["FlowerSort"]] = relationship(back_populates="type")
    


class FlowerSort(Base):
    __tablename__ = "flower_sort"
    
    type_name: Mapped[str] = mapped_column(
        ForeignKey("flower_type.name"), primary_key=True
    )
    sort_name: Mapped[str] = mapped_column(
        primary_key=True
    )
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    type: Mapped["Flower"] = relationship(back_populates="sorts")
    
    
class BoxType(Base):
    __tablename__ = "box_type"
    
    type: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)


class Plantation(Base):
    __tablename__ = "plantation"
    
    name: Mapped[str] = mapped_column(
        primary_key=True
    )
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    

class Agencie(Base):
    __tablename__ = "agencie"
    
    name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="agencie")
    
    
class Truck(Base):
    __tablename__ = "truck"
    
    name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    outcomes: Mapped[list["Outcome"]] = relationship(back_populates="truck")


class OrderType(Base):
    __tablename__ = "order_type"
    
    name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    orders: Mapped[list["Order"]] = relationship(back_populates="type")
