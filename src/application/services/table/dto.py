from src.application.common.dto import DataTransferObject
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.box.dto.box import Box as BoxDTO
from src.application.flower_in_box.dto.flower_in_box import FlowerInBox


class Flower(DataTransferObject):
    flower: FlowerInBox


class Box(DataTransferObject):
    box_data: BoxDTO
    flowers: list[Flower]


class Invoice(DataTransferObject):
    invoice_data: IncomeInvoice
    boxes: list[Box]


class TableDTO(DataTransferObject):
    invoices: list[Invoice]
