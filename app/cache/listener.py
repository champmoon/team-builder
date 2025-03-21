import logging

from redis.asyncio.lock import Lock

# from app.api.tasks import dispath_tasks
from app.cache.connection import get_connection

logger = logging.getLogger(__name__)

LOCK_TIMEOUT = 3
LOCK_PREFIX = "lock_"


async def listen_redis_key_expired() -> None:
    async_connections_gen = get_connection()
    async_connection = await anext(async_connections_gen)
    pubsub = async_connection.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")

    async for msg in pubsub.listen():
        try:
            key: str = msg["data"].decode("utf-8")
            if key.startswith(LOCK_PREFIX):
                continue

            redis_lock: Lock = async_connection.lock(
                name=LOCK_PREFIX + key,
                timeout=LOCK_TIMEOUT,
                blocking=False,
            )

            if await redis_lock.locked():
                continue

            is_acquired = await redis_lock.acquire()
            if not is_acquired:
                continue

            # await dispath_tasks(key=key)

        except Exception as e:
            logger.error(e)
