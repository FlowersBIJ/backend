from src.application.common.dto import DataTransferObject
from src.application.client.dto.client import Client as ClientDTO
from src.application.order.dto.order import Order as OrderDTO
from src.application.income_invoice.dto.income_invoice import IncomeInvoice
from src.application.box.dto.box import Box as BoxDTO
from src.application.flower_in_box.dto.flower_in_box import FlowerInBox


class Flower(DataTransferObject):
    flower: FlowerInBox


class Box(DataTransferObject):
    box_data: BoxDTO
    invoice: IncomeInvoice
    flowers: list[Flower]


class Order(DataTransferObject):
    order_data: OrderDTO
    boxes: list[Box]


class Client(DataTransferObject):
    client_data: ClientDTO
    orders: list[Order]


class TableDTO(DataTransferObject):
    clients: list[Client]
