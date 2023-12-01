import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.models.base import Base

if TYPE_CHECKING:
    from src.infra.database.models.order import Order
    from src.infra.database.models.flower import FlowerInBox
    

class BoxType(Base):
    __tablename__ = "box_types"
    
    typename: Mapped[str] = mapped_column(primary_key=True)
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    boxes: Mapped[list["Box"]] = relationship(back_populates="box")


class Plantation(Base):
    __tablename__ = "plantations"
    
    plantation_name: Mapped[str] = mapped_column(
        primary_key=True
    )
    visible: Mapped[bool] = mapped_column(default=True, nullable=False)

    invoices: Mapped[list["IncomeInvoice"]] = relationship(back_populates="plant")
   
   
class IncomeInvoice(Base):
    __tablename__ = "income_invoices"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4()
    )
    invoice: Mapped[str] = mapped_column(nullable=False)
    plantation: Mapped[str] = mapped_column(ForeignKey("plantations.plantation_name"), nullable=False)
    
    plant: Mapped[Plantation] = relationship(back_populates="invoices")
    boxes: Mapped[list["Box"]] = relationship(back_populates="invoice")
    
   
class Box(Base):
    __tablename__ = "boxes"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4()
    )
    
    release_date: Mapped[date] = mapped_column(nullable=True)
    box_count: Mapped[int] = mapped_column(nullable=False)
    
    visible: Mapped[bool] = mapped_column(nullable=False, default=True)
    box_type: Mapped[str] = mapped_column(
        ForeignKey("box_types.name"), nullable=True
    )
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("income_invoices.id"), nullable=True)
    
    flowers: Mapped[list[FlowerInBox]] = relationship(back_populates="box")
    box: Mapped[BoxType] = relationship(back_populates="boxes")
    invoice: Mapped[IncomeInvoice] = relationship(back_populates="boxes")
    order: Mapped[Order] = relationship(back_populates="boxes")
   