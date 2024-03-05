from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import sportsman_urls_router, trainer_urls_router
from .conf.settings import settings
from .containers import wire_containers
from .docs import app_docs, sportsmans_api_docs, trainers_api_docs

wire_containers()

trainers_api = FastAPI(
    version=settings.VERSION,
    title=trainers_api_docs["title"],
    description=trainers_api_docs["description"],
    debug=settings.DEBUG,
)
trainers_api.include_router(trainer_urls_router, prefix=settings.API_PREFIX)

sportsmans_api = FastAPI(
    version=settings.VERSION,
    title=sportsmans_api_docs["title"],
    description=sportsmans_api_docs["description"],
    debug=settings.DEBUG,
)
sportsmans_api.include_router(sportsman_urls_router, prefix=settings.API_PREFIX)

app = FastAPI(
    version=settings.VERSION,
    title=app_docs["title"],
    description=app_docs["description"],
    debug=settings.DEBUG,
    docs_url="/",
)

app.mount(path="/trainers", app=trainers_api)
app.mount(path="/sportsmans", app=sportsmans_api)


app.mount(
    settings.STATIC_FILES_DIR,
    StaticFiles(directory=settings.STATIC_FILES_DIR[1:]),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"],
    allow_headers=["*"],
)

if settings.DEBUG:
    app.mount("/" + settings.FILES_DIR, StaticFiles(directory=settings.FILES_DIR))

    from .utils import log_middleware

    app.middleware(middleware_type="http")(log_middleware)

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
