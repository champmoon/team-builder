import logging
from pprint import pformat
from typing import Any

from fastapi import Request, Response
from pydantic import Json
from starlette.background import BackgroundTask
from starlette.types import Message

from app.schemas.base_class import BaseSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("log")


IGNORE_URLS = (
    "/docs",
    "/openapi.json",
)


class RequestInfo(BaseSchema):
    path: str
    headers: dict
    body: Json


class ResponseInfo(BaseSchema):
    status_code: int
    body: Json


def log_info(request_info: RequestInfo, response_info: ResponseInfo) -> None:
    logger.info(pformat(request_info.model_dump()))
    logger.info(pformat(response_info.model_dump()))


async def log_middleware(request: Request, call_next: Any) -> Response:
    request_body = await request.body()

    await set_body(request=request, body=request_body)

    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    log_task = None
    if not request.url.path in IGNORE_URLS:
        log_task = BackgroundTask(
            log_info,
            RequestInfo(
                path=request.url.path,
                headers=request.headers,
                body=request_body,
            ),
            ResponseInfo(
                status_code=response.status_code,
                body=response_body,
            ),
        )

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=log_task,
    )


async def set_body(request: Request, body: bytes) -> None:
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive
