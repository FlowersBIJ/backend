from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.models.base import Base

if TYPE_CHECKING:
    from src.infra.database.models.order import Order



class Agencie(Base):
    __tablename__ = "agencies"
    
    agencie_name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    clients: Mapped[list["Client"]] = relationship(back_populates="ag")
    
    
class Truck(Base):
    __tablename__ = "trucks"
    
    truck_name: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    clients: Mapped[list["Client"]] = relationship(back_populates="tr")
    
    
class Client(Base):
    __tablename__ = "clients"
    
    client_name: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    alternative_name: Mapped[str] = mapped_column(nullable=True)
    
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=True)
    
    agencie: Mapped[str] = mapped_column(ForeignKey("agencie.name"), nullable=True)
    truck: Mapped[str] = mapped_column(ForeignKey("truck.name"), nullable=True)
    
    ag: Mapped[Agencie] = relationship(back_populates="clients")
    tr: Mapped[Truck] = relationship(back_populates="clients")
    orders: Mapped[list[Order]] = relationship(back_populates="client")
