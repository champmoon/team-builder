import logging
import pprint as pp
from typing import Any, Literal

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
    "/files/database.png",
)


class RequestInfo(BaseSchema):
    path: str
    headers: dict
    body: Json | None = None


class ResponseInfo(BaseSchema):
    status_code: int
    body: Json | None = None


def log_info(request_info: RequestInfo, response_info: ResponseInfo) -> None:
    logger.info(f"\nREQUEST:  {request_info.model_dump_json()}\n")
    logger.info(f"\nRESPONSE: {response_info.model_dump_json()}\n")


async def log_middleware(request: Request, call_next: Any) -> Response:
    request_body = await request.body()

    await set_body(request=request, body=request_body)

    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    log_task = None
    if request.url.path not in IGNORE_URLS:
        log_task = BackgroundTask(
            log_info,
            RequestInfo(
                path=request.url.path,
                headers=request.headers,
                body=request_body or None,
            ),
            ResponseInfo(
                status_code=response.status_code,
                body=response_body or None,
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
