from typing import Any

from fastapi import FastAPI, Depends, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.log import log
from src.presentation.exceptions import setup_exception_handlers
from src.presentation.routers.middlewares import LoggingMiddleware


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
    # configure_routers(
    #     app=app,
    #     prefix=prefix,
    #     auth_enabled=False,
    #     routers=[
    #
    #     ],
    # )

    setup_exception_handlers(app)


def setup_middlewares(app: FastAPI) -> None:
    logging_middleware = LoggingMiddleware(logger=log())
    app.add_middleware(
        BaseHTTPMiddleware, dispatch=logging_middleware
    )
