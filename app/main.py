from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import urls_router
from .conf.settings import settings
from .containers import wire_containers
from .docs import app_docs

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
wire_containers()

if settings.DEBUG:
    app.mount("/" + settings.FILES_DIR, StaticFiles(directory=settings.FILES_DIR))

    from .utils import log_middleware

    app.middleware("http")(log_middleware)

if not settings.DEBUG:
    import logging

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(gunicorn_logger.level)


# TODO when sportsman added to group, group workout should be on new sportsman
# TODO make workouts statuses api
# TODO update workouts
# TODO delete workouts when deletinig group, sportsman from team
# TODO bind workout to other categories
# TODO create workouts api for sportsman
# TODO make trainers -> sportsmans api
# TODO make update workouts statuses(cache)

# TODO make transaction
# TODO make tests
