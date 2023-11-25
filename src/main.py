import asyncio
import os

from src.app import Application
from src.application.common.exceptions import ApplicationException
from src.infra.log import log

logger = log()


async def run() -> None:
    settings_path = os.getenv("SETTINGS")
    if settings_path is None:
        raise ApplicationException("Settings environment not specified")
    app = await Application.from_config(settings_path)

    try:
        await app.start()
    finally:
        await app.dispose()


def main() -> None:
    try:
        asyncio.run(run())
        exit(0)
    except SystemExit:
        exit(0)
    except ApplicationException:
        exit(70)
    except BaseException:
        logger.exception("Unexpected error occured")
        exit(70)


if __name__ == "__main__":
    main()
