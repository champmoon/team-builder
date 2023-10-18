from pydantic import RedisDsn, validator
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str

    ASYNC_REDIS_CACHE_URI: RedisDsn | None = None

    @validator("ASYNC_REDIS_CACHE_URI", pre=True)
    def assemble_cache_connection(
        cls, v: RedisDsn | None, values: dict[str, str]
    ) -> RedisDsn:
        if v:
            return v
        return RedisDsn.build(
            scheme="redis",
            password=values["REDIS_PASSWORD"],
            host=values["REDIS_HOST"],
            port=int(values["REDIS_PORT"]),
        )
