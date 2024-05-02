import asyncio
from typing import Any

from fastapi import FastAPI, Request, applications
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .api.urls import urls_router
from .cache.listener import listen_redis_key_expired
from .conf.settings import settings
from .containers import wire_containers
from .docs import app_docs
from .utils import log_middleware

wire_containers()

app = FastAPI(
    version=settings.VERSION,
    title=app_docs["title"],
    description=app_docs["description"],
    debug=settings.DEBUG,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"],
    allow_headers=["*"],
)
app.include_router(urls_router, prefix=settings.API_PREFIX)


app.mount(
    "/" + settings.STATIC_FILES_DIR,
    StaticFiles(directory=settings.STATIC_FILES_DIR),
)
app.mount(
    "/" + settings.FILES_DIR,
    StaticFiles(directory=settings.FILES_DIR),
)
app.mount(
    "/",
    StaticFiles(directory="spa", html=True),
)


app.middleware(middleware_type="http")(log_middleware)


@app.middleware("http")
async def add_version_header(request: Request, call_next: Any) -> Any:
    if any((
        "api" in request["path"],
        "static" in request["path"],
        "assets" in request["path"],
        "icons" in request["path"],
        "files" in request["path"],
        "docs" in request["path"],
        "redoc" in request["path"],
        "openapi.json" in request["path"],
    )):
        return await call_next(request)

    return FileResponse("spa/index.html")


if not settings.DEBUG:
    import logging

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(gunicorn_logger.level)


@app.on_event("startup")
async def startup_event() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(listen_redis_key_expired())


def swagger_monkey_patch(*args: Any, **kwargs: Any) -> Any:
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url=(
            "https://gcore.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"
        ),
        swagger_css_url=(
            "https://gcore.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
        ),
    )


applications.get_swagger_ui_html = swagger_monkey_patch


# TODO when sportsman added to group, group workout should be on new sportsman
# TODO make workouts statuses api
# TODO delete workouts when deletinig group, sportsman from team
# TODO make update workouts statuses(cache)
