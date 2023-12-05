from src.application.common.filters.filter import Filters
from src.application.services.table.dto import TableDTO, Client, Order, Box, Flower

from src.application.client.interfaces.client_reader import ClientReader
from src.application.order.interfaces.order_reader import OrderReader
from src.application.income_invoice.interfaces.income_invoice_reader import (
    IncomeInvoiceReader,
)
from src.application.box.interfaces.box_reader import BoxReader
from src.application.flower_in_box.interfaces.flower_in_box_reader import (
    FlowerInBoxReader,
)


class Table:
    def __init__(
        self,
        client_reader: ClientReader,
        order_reader: OrderReader,
        invoice_reader: IncomeInvoiceReader,
        box_reader: BoxReader,
        flower_in_box_reader: FlowerInBoxReader,
    ) -> None:
        self.client_reader = client_reader
        self.order_reader = order_reader
        self.invoice_reader = invoice_reader
        self.box_reader = box_reader
        self.flower_in_box_reader = flower_in_box_reader

    async def get_table(self, is_visible=True):
        clients_list = await self.client_reader.get_clients(
            filters=Filters(
                offset=0, limit=await self.client_reader.get_count(), visible=is_visible
            )
        )
        orders_list = await self.order_reader.get_orders(
            filters=Filters(
                offset=0, limit=await self.order_reader.get_count(), visible=is_visible
            )
        )
        invoices_list = await self.invoice_reader.get_invoices(
            filters=Filters(
                offset=0,
                limit=await self.invoice_reader.get_count(),
                visible=is_visible,
            )
        )
        boxes_list = await self.box_reader.get_boxes(
            filters=Filters(
                offset=0,
                limit=await self.box_reader.get_count(),
                visible=is_visible,
            )
        )
        flowers_list = await self.flower_in_box_reader.get_flowers(
            filters=Filters(
                offset=0,
                limit=await self.flower_in_box_reader.get_count(),
                visible=is_visible,
            )
        )

        return TableDTO(
            clients=[
                Client(
                    client_data=client,
                    orders=[
                        Order(
                            order_data=order,
                            boxes=[
                                Box(
                                    box_data=box,
                                    invoice=next(
                                        (
                                            invoice
                                            for invoice in invoices_list.invoices
                                            if invoice.id == box.invoice_id
                                        ),
                                        None,
                                    ),
                                    flowers=[
                                        Flower(
                                            flower=flower,
                                            total=flower.income_price * flower.stems,
                                            total_sale=flower.outcome_price
                                            * flower.stems
                                            if flower.hotline_miami_price is None
                                            else flower.hotline_miami_price
                                            * flower.stems,
                                            difference=(
                                                flower.outcome_price * flower.stems
                                                if flower.hotline_miami_price is None
                                                else flower.hotline_miami_price
                                                * flower.stems
                                            )
                                            - flower.income_price * flower.stems,
                                        )
                                        for flower in flowers_list.flowers
                                        if flower.box_id == box.id
                                    ],
                                )
                                for box in boxes_list.boxes
                                if box.order_id == order.id
                            ],
                        )
                        for order in orders_list.orders
                        if order.client_name == client.client_name
                    ],
                )
                for client in clients_list.clients
            ]
        )
