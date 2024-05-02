from contextlib import AbstractAsyncContextManager
from typing import Callable

from redis.asyncio import Redis as AIORedis


class HealthQuestionnaireAction:
    def __init__(
        self,
        sportsman_id: str,
        connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
        health_questionnaire_id: str = "",
    ) -> None:
        self.connection_factory = connection_factory

        self.sportsman_id = sportsman_id
        self.health_questionnaire_id = health_questionnaire_id

        self.pre_key = self._create_pre_key(sportsman_id=sportsman_id)
        self.full_key = self._create_full_key(
            sportsman_id=sportsman_id,
            health_questionnaire_id=health_questionnaire_id,
        )
        self.sportsman_key_match = self._create_sportsman_key_match(
            sportsman_id=sportsman_id
        )

    def _create_pre_key(self, sportsman_id: str) -> str:
        return f"pre_health_questionnaire_{sportsman_id}"

    def _create_full_key(self, sportsman_id: str, health_questionnaire_id: str) -> str:
        return f"health_questionnaire_{sportsman_id}_{health_questionnaire_id}"

    def _create_sportsman_key_match(self, sportsman_id: str) -> str:
        return f"health_questionnaire_{sportsman_id}_*"

    async def get_health_qs(self) -> str | None:
        async with self.connection_factory() as connection:
            all_qs_mathes = connection.scan_iter(self.sportsman_key_match)

        shift_len = len(self.sportsman_key_match) - 1
        questionnaire_ids: list[str] = []
        async for qs_math in all_qs_mathes:
            questionnaire_ids.append(qs_math.decode()[shift_len:])

        assert len(questionnaire_ids) < 2

        if len(questionnaire_ids) == 0:
            return None

        return questionnaire_ids[0]

    async def set_pre(self, timeout: int) -> None:
        async with self.connection_factory() as connection:
            await connection.set(self.pre_key, self.pre_key, ex=timeout)

    async def set_full(self, timeout: int = 86400) -> None:
        async with self.connection_factory() as connection:
            await connection.set(self.full_key, self.full_key, ex=timeout)

    async def rmv_full(self) -> None:
        async with self.connection_factory() as connection:
            await connection.delete(self.full_key)

    async def is_set_pre(self) -> bool:
        async with self.connection_factory() as connection:
            raw_data = await connection.get(self.pre_key)

        return True if raw_data else False

    async def is_set_full(self) -> bool:
        async with self.connection_factory() as connection:
            raw_data = await connection.get(self.full_key)

        return True if raw_data else False

    # async def ttl(self) -> int:
    #     async with self.connection_factory() as connection:
    #         return int(await connection.ttl(self.key))
