import json
from contextlib import AbstractAsyncContextManager
from enum import StrEnum
from typing import Callable, Generic, Type, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis as AIORedis


class ActionTypes(StrEnum):
    CHECK_CONFIRM_EMAIL = "check_confirm_email"
    # CONFIRM_TRAINER_EMAIL = "confirm_trainer_email"
    # CONFIRM_SPORTSMAN_EMAIL = "confirm_sportsman_email"
    CONFIRM_EMAIL = "confirm_email"
    GET_CONFIRM_EMAIL = "get_confirm_email"
    LIMIT_EMAIL = "limit_email"
    LIMIT_LOGIN = "limit_login"
    RESET_EMAIL = "reset_email"
    RESET_PASSWORD = "reset_password"
    INVITE = "invite"


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
