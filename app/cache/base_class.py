import json
from contextlib import AbstractAsyncContextManager
from enum import StrEnum
from functools import partial
from typing import Callable, Generic, Type, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis as AIORedis


class ActionTypes(StrEnum):
    LIMIT_LOGIN = "limit_login"
    CONFIRM_EMAIL = "confirm_email"
    CHECK_CONFIRM_EMAIL = "check_confirm_email"
    RESET_EMAIL = "reset_email"
    RESET_PASSWORD = "reset_password"
    LIMIT_EMAIL = "limit_email"
    CHECK_WS = "check_websocket"
    RELATE_OBJ = "relate_obj"
    RELATE_TOKENS_USER = "relate_tokens_user"
    RELATE_TOKENS_DEVICE = "relate_tokens_device"
    RELATE_DEVICES_USER = "relate_devices_user"


class BaseActionData(BaseModel): ...


BaseActionDataType = TypeVar("BaseActionDataType", bound=BaseActionData)


class BaseAction(Generic[BaseActionDataType]):
    timeout: int | None = None

    action_type: ActionTypes
    action_data: Type[BaseActionDataType]

    def __init__(
        self,
        key: str,
        connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
    ) -> None:
        self.connection_factory = connection_factory
        self.key = self._create_unique_key(key=key)

    def _create_unique_key(self, key: str) -> str:
        return f"{self.action_type}_{key}"

    async def get(self) -> BaseActionDataType | None:
        async with self.connection_factory() as connection:
            raw_data = await connection.get(self.key)

        if not raw_data:
            return None

        return self.action_data(**json.loads(raw_data))

    async def set(self, new_action_data: BaseActionDataType) -> None:
        async with self.connection_factory() as connection:
            await connection.set(
                self.key, new_action_data.model_dump_json(), ex=self.timeout
            )

    async def rmv(self) -> None:
        async with self.connection_factory() as connection:
            await connection.delete(self.key)

    async def ttl(self) -> int:
        async with self.connection_factory() as connection:
            return int(await connection.ttl(self.key))


def create_action(
    action_class: Type[BaseAction],
    connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
) -> Callable[[str], BaseAction]:
    return partial(action_class, connection_factory=connection_factory)
