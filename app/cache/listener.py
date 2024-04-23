import asyncio

import logging
from app.cache.connection import get_connection

logger = logging.getLogger(__name__)


async def listen_redis_key_expired() -> None:
    async_connections_gen = get_connection()
    async_connection = await anext(async_connections_gen)
    pubsub = async_connection.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")

    async for msg in pubsub.listen():
        logger.info(f"\nREDIS MESSAGE - {msg}\n")
        try:
            session = msg["data"].decode("utf-8")
            print(session)

        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    asyncio.run(listen_redis_key_expired())
