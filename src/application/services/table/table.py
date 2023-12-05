from src.application.common.filters.filter import Filters
from src.application.services.table.dto import TableDTO, Invoice, Box, Flower

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
        invoice_reader: IncomeInvoiceReader,
        box_reader: BoxReader,
        flower_in_box_reader: FlowerInBoxReader,
    ) -> None:
        self.invoice_reader = invoice_reader
        self.box_reader = box_reader
        self.flower_in_box_reader = flower_in_box_reader

    async def get_table(self, is_visible=True):
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
            invoices=[
                Invoice(
                    invoice_data=invoice,
                    boxes=[
                        Box(
                            box_data=box,
                            flowers=[
                                Flower(flower=flower)
                                for flower in flowers_list.flowers
                                if flower.box_id == box.id
                            ],
                        )
                        for box in boxes_list.boxes
                        if box.invoice_id == invoice.id
                    ],
                )
                for invoice in invoices_list.invoices
            ]
        )
