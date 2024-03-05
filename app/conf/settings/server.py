import tomllib

from pydantic import HttpUrl, validator
from pydantic_settings import BaseSettings


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        return str(data["tool"]["poetry"]["version"])


class ServerSettings(BaseSettings):
    VERSION: str = ""
    API_PREFIX: str = "/api"

    PROTOCOL: str = "http"
    SERVER_HOST: str
    SERVER_PORT: str

    DEBUG: bool

    FILES_DIR: str = "files"

    @validator("VERSION", pre=True)
    def get_app_version(cls, v: str | None, values: dict[str, str]) -> str:
        if v:
            return v
        return get_version()

    SERVER_HOSTNAME: str | None = None

    @validator("SERVER_HOSTNAME", pre=True)
    def assemble_server_(cls, v: str | None, values: dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return str(
            HttpUrl.build(
                scheme=values["PROTOCOL"],
                host=values["SERVER_HOST"],
                port=int(values["SERVER_PORT"]),
            )
        )

    STATIC_FILES_DIR: str = "static"
