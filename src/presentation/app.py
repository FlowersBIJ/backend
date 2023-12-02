from typing import Any

from fastapi import APIRouter, Depends, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.log import log
from src.presentation.exceptions import setup_exception_handlers
from src.presentation.routers.agencie.v1 import agencies
from src.presentation.routers.box.v1 import boxes
from src.presentation.routers.box_type.v1 import box_types
from src.presentation.routers.client.v1 import clients
from src.presentation.routers.flower.v1 import flowers
from src.presentation.routers.flower_in_box.v1 import flowers_in_box
from src.presentation.routers.flower_length.v1 import flowers_length
from src.presentation.routers.flower_sort.v1 import flowers_sort
from src.presentation.routers.income_invoice.v1 import income_invoices
from src.presentation.routers.middlewares import LoggingMiddleware
from src.presentation.routers.order.v1 import orders
from src.presentation.routers.order_type.v1 import order_types
from src.presentation.routers.plantation.v1 import plantations
from src.presentation.routers.truck.v1 import trucks


def configure_routers(
    app: FastAPI, prefix: str, auth_enabled: bool, routers: list[APIRouter]
):
    # DEPENDENCIES = [Depends(has_access)]
    DEPENDENCIES: Any = []
    for router in routers:
        app.include_router(
            router=router,
            prefix=prefix,
            dependencies=DEPENDENCIES if auth_enabled else None,
        )


def setup_routers(app: FastAPI, prefix: str) -> None:
    # app.include_router(router=auth, prefix=prefix)
    # app.include_router(router=users, prefix=prefix)
    configure_routers(
        app=app,
        prefix=prefix,
        auth_enabled=False,
        routers=[
            agencies,
            boxes,
            box_types,
            clients,
            flowers,
            flowers_in_box,
            flowers_length,
            flowers_sort,
            income_invoices,
            orders,
            order_types,
            plantations,
            trucks
        ],
    )

    setup_exception_handlers(app)


def setup_middlewares(app: FastAPI) -> None:
    logging_middleware = LoggingMiddleware(logger=log())
    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
