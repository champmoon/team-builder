import asyncio
import logging
from datetime import timedelta

import sqlalchemy as sa
from tenacity import retry
from tenacity.after import after_log
from tenacity.before import before_log
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from app.db.session import async_engine

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

max_tries = timedelta(seconds=60).seconds
wait_seconds = timedelta(seconds=1).seconds


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def health() -> None:
    try:
        async with async_engine.connect() as conn:
            await conn.execute(sa.text("SELECT 1"))
            logger.info("ok...")
        await async_engine.dispose()

    except Exception as e:
        logger.info("error...")
        logger.error(e)
        raise e


if __name__ == "__main__":
    asyncio.run(health())
