import asyncio
import logging

import uvicorn
from dynaconf import Dynaconf  # type: ignore
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.cors import CORSMiddleware

from src.exceptions import DisposeException, StartServerException
from src.infra.auth.auth import CasdoorAuth
from src.infra.database.session import setup_database
from src.infra.log import log
from src.presentation.app import setup_middlewares, setup_routers


class Application:
    def __init__(
        self,
        config: Dynaconf,
        app: FastAPI,
        sqlalchemy_engine: AsyncEngine,
        auth: CasdoorAuth,
    ) -> None:
        self._config = config
        self._app = app
        self._sqlalchemy_engine = sqlalchemy_engine
        self._auth = auth

    @classmethod
    async def from_config(cls, settings_path: str) -> "Application":
        config = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[settings_path + "/settings.toml"],
        )

        logger = log(level=config.log.level)
        logger.info("Creating sqlalchemy engine")
        session_local, sqlalchemy_engine = setup_database(config.database.url)

        logger.info("Initializing application")
        app = FastAPI(
            title=config.api.project_name, docs_url=config.api.prefix + "/docs"
        )

        app.state.db_session = session_local
        app.state.config = config

        logger.info("Initializing middlewares")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.api.backend_cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logger.info("Initializing routes und middlewares")
        setup_routers(app, config.api.prefix)
        setup_middlewares(app)

        logger.info("Initializing auth application")
        auth = CasdoorAuth(
            endpoint=config.casdoor.endpoint,
            client_id=config.casdoor.client_id,
            client_secret=config.casdoor.client_secret,
            certificate=config.casdoor.certificate,
            org_name=config.casdoor.org_name,
            application_name=config.api.project_name,
            front_endpoint=config.casdoor.front_endpoint
        )
        logger.info("Initializing auth finished")

        logger.info("Creating application")
        application = Application(
            config=config, app=app, sqlalchemy_engine=sqlalchemy_engine, auth=auth
        )

        logger.info("Initializing application finished")

        return application

    async def start(self) -> None:
        await self.start_app()

    async def start_app(self) -> None:
        logger = log()
        logger.info("HTTP server is starting")

        try:
            server = uvicorn.Server(
                config=uvicorn.Config(
                    app=self._app,
                    host=self._config.api.host,
                    port=int(self._config.api.port),
                )
            )
            logger_access = logging.getLogger("uvicorn.access")
            logger_access.disabled = True
            logger_errors = logging.getLogger("uvicorn.error")
            logger_errors.disabled = True

            await server.serve()
        except asyncio.CancelledError:
            logger.info("HTTP server has been interrupted")
        except BaseException as unexpected_error:
            logger.exception("HTTP server failed to start")

            raise StartServerException from unexpected_error

    async def dispose(self) -> None:
        logger = log()

        logger.info("Application is shutting down...")

        dispose_errors = []

        logger.info("Disposing SQLAlchemy client")
        try:
            await self._sqlalchemy_engine.dispose()
        except Exception as unexpected_error:
            dispose_errors.append(unexpected_error)
            logger.exception("Failed to dispose SQLAlchemy client")
        else:
            logger.info("SQLAlchemy client has been disposed")

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            raise DisposeException(
                "Application has shut down with errors, see logs above"
            )

        logger.info("Application has successfully shut down")
