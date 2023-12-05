from dynaconf import Dynaconf

from src.infra.casdoor.auth import JWTValidatorService


async def setup_casdoor(config: Dynaconf):
    return JWTValidatorService(
        config.casdoor.endpoint,
        config.casdoor.client_id,
        config.casdoor.client_secret,
        config.casdoor.certificate,
        config.casdoor.org_name,
        config.api.project_name,
        config.casdoor.front_endpoint,
    )
