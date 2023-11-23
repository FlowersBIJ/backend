from casdoor import AsyncCasdoorSDK
from dynaconf import Dynaconf

from src.infra.log import log


class Auth:
    def __init__(
            self,
            config: Dynaconf,
            sdk: AsyncCasdoorSDK
    ) -> None:
        self._config = config
        self._sdk = sdk

    @classmethod
    async def from_config(cls, settings_path: str) -> "Auth":
        config = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[
                settings_path + "/settings.toml"
            ],
        )

        logger = log(level=config.log.level)
        logger.info("Initializing auth app")
        sdk = AsyncCasdoorSDK(
            endpoint=config.casdoor.endpoint,
            client_id=config.casdoor.client_id,
            client_secret=config.casdoor.client_secret,
            certificate=config.casdoor.certificate,
            org_name=config.casdoor.org_name,
            application_name=config.api.project_name
        )
        logger.info("Initializing auth app finished")
        auth = Auth(
            config=config,
            sdk=sdk
        )

        return auth
