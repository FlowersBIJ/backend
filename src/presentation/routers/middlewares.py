from starlette.requests import Request
from starlette.responses import Response
from structlog.stdlib import BoundLogger


class LoggingMiddleware:
    def __init__(self, logger: BoundLogger):
        self.log = logger

    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        response_body = b""

        async for chunk in response.body_iterator:
            response_body += chunk

        decoded_resp = response_body.decode()

        self.log.info(
            status=response.status_code,
            content=decoded_resp,
            headers=response.headers
        )
        return Response(status_code=response.status_code, content=response_body, headers=response.headers,
                        media_type=response.media_type)
