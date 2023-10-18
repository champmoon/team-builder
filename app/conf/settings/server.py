import tomllib

from pydantic import validator
from pydantic_settings import BaseSettings


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        return str(data["tool"]["poetry"]["version"])


class ServerSettings(BaseSettings):
    VERSION: str | None = None
    API_PREFIX: str = "/api"

    SERVER_HOST: str
    SERVER_PORT: str

    DEBUG: bool

    @validator("VERSION", pre=True)
    def get_app_version(cls, v: str | None, values: dict[str, str]) -> str:
        if v:
            return v
        return get_version()
