"""
Server app config
"""
from __future__ import annotations

import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.infra.postgres.retort import UserRetort
from src.infra.postgres.setup import setup_postgres

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    @classmethod
    async def from_config(cls) -> Application:  # a.k.a startup

        logger.info("Initializing application")
        app = FastAPI()

        logger.info("Initializing middlewares")

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logger.info("Initializing exeception handlers")
        # TODO: реализовать обработку исключений

        logger.info("Initializing postgres connection pool")
        pool = await setup_postgres()
        app.state.pool = lambda: pool

        logger.info("Initializing type converters")
        user_retort = UserRetort()
        app.state.user_retort = lambda: user_retort
        application = Application(app=app)

        logger.info("Initializing application finished")

        logger.info(f"Cprocessing config - {config.dict()}")

        return application

    async def start(self) -> None:
        logger.info("HTTP server is starting")

        try:
            server = uvicorn.Server(
                config=uvicorn.Config(
                    app=self.app,
                    host="0.0.0.0",
                    port=int(self.config.API_PORT),
                )
            )
            await server.serve()
        except asyncio.CancelledError:
            logger.info("HTTP server has been interrupted")
        except BaseException as unexpected_error:
            logger.exception("HTTP server failed to start")

            raise StartServerException from unexpected_error

    async def dispose(self) -> None:
        logger.info("Application is shutting down...")

        dispose_errors: list[str] = []

        # TODO: закрыть все соединения\освободить все ресурсы

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            raise DisposeException(
                "Application has shut down with errors, see logs above"
            )

        logger.info("Application has successfully shut down")
