from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable

from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as AIORedis

from app.conf.settings import settings


def async_connectionmaker(
    connection_pool: ConnectionPool,
    encoding: str,
    decode_responses: bool,
    **kwargs: Any,
) -> Callable[[], AIORedis]:
    def create_connection() -> AIORedis:
        return AIORedis(
            connection_pool=connection_pool,
            encoding=encoding,
            decode_responses=decode_responses,
            **kwargs,
        )

    return create_connection


pool = ConnectionPool.from_url(url=str(settings.ASYNC_REDIS_CACHE_URI))

async_connection = async_connectionmaker(
    connection_pool=pool, encoding="utf-8", decode_responses=True
)


async def get_connection() -> AsyncGenerator[AIORedis, None]:
    async with async_connection() as connection:
        yield connection


class Cache:
    def __init__(self) -> None:
        self._connection_factory = async_connection

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[AIORedis, None]:
        connection: AIORedis = self._connection_factory()
        try:
            yield connection
        finally:
            await connection.close()
