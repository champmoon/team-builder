from pydantic import Extra
from pydantic_settings import SettingsConfigDict

from .admin import AdminSettings
from .email import EmailSettings
from .jwt import JWTSettings
from .postgres import PostgresSettings
from .redis import RedisSettings
from .server import ServerSettings


class Settings(
    AdminSettings,
    EmailSettings,
    JWTSettings,
    PostgresSettings,
    RedisSettings,
    ServerSettings,
):
    model_config = SettingsConfigDict(env_file=".env", extra=Extra.allow)


settings = Settings()
