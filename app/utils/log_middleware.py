import json
import logging
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
    "/files/database.png",
)


class RequestInfo(BaseSchema):
    headers: dict
    body: Json | None = None


class ResponseInfo(BaseSchema):
    status_code: int
    body: Json | None = None


def log_info(request_info: RequestInfo, response_info: ResponseInfo, path: str) -> None:
    full_info = {
        "PATH": path,
        "REQUEST": request_info.model_dump(),
        "RESPONSE": response_info.model_dump(),
    }
    logger.info(f"\n\n {json.dumps(full_info)} \n\n")


async def log_middleware(request: Request, call_next: Any) -> Response:
    request_body = await request.body()

    await set_body(request=request, body=request_body)

    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    log_task = None
    if request.url.path not in IGNORE_URLS:
        try:
            log_task = BackgroundTask(
                log_info,
                RequestInfo(
                    headers=request.headers,  # type: ignore
                    body=request_body or None,
                ),
                ResponseInfo(
                    status_code=response.status_code,
                    body=response_body or None,
                ),
                request.url.path,
            )
        except Exception as e:
            logger.error(f"\n\n {str(e)} \n\n")

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
