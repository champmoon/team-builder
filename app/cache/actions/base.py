from typing import Any

import json
from contextlib import AbstractAsyncContextManager
from enum import StrEnum
from functools import partial
from typing import Callable, Generic, Type, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis as AIORedis


def create_action(
    action_class: Any,
    connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
) -> Callable[[str], Any]:
    return partial(action_class, connection_factory=connection_factory)
