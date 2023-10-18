from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Coroutine

from typing_extensions import ParamSpec

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


_P = ParamSpec("_P")


class Background:
    max_threads: int | None = None

    def __new__(cls) -> Background:
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor(max_workers=self.max_threads)

    def run(self, coro: Coroutine) -> None:
        logger.info(f"Run coroutine - {coro.__name__} in the background")

        new_loop = asyncio.new_event_loop()
        new_loop.run_in_executor(self.executor, asyncio.run, coro)

    def run_sync(
        self, func: Callable[_P, Any], *args: _P.args, **kwargs: _P.kwargs
    ) -> None:
        logger.info(f"Run function - {func.__name__} in the background")

        new_loop = asyncio.new_event_loop()
        new_loop.run_in_executor(self.executor, func, *args, **kwargs)
