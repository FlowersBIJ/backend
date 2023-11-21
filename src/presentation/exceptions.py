from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.infra.database.repositories.exceptions import (
    EntityNotFoundException,
    EntityUpdateException,
    EntityCreateException,
    EntityDeleteException,
)


async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
    return JSONResponse(status_code=404, content=exc.message)


async def entity_update_error_handler(request: Request, exc: EntityUpdateException):
    return JSONResponse(status_code=422, content=exc.message)


async def entity_creation_error_handler(request: Request, exc: EntityCreateException):
    return JSONResponse(status_code=422, content=exc.message)


async def entity_deletion_error_handler(request: Request, exc: EntityDeleteException):
    return JSONResponse(status_code=406, content=exc.message)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=EntityNotFoundException,
        handler=entity_not_found_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityUpdateException,
        handler=entity_update_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityCreateException,
        handler=entity_creation_error_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityDeleteException,
        handler=entity_deletion_error_handler,
    )