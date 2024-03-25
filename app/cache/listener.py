from .connection import get_connection
import logging

logger = logging.getLogger(__name__)


async def listen_redis_key_expired() -> None:
    async_connections_gen = get_connection()
    async_connection = await anext(async_connections_gen)
    pubsub = async_connection.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")

    async for msg in pubsub.listen():
        logger.info(f"\nREDIS MESSAGE - {msg}\n")
