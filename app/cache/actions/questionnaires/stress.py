import json
from contextlib import AbstractAsyncContextManager
from enum import StrEnum
from functools import partial
from typing import Callable, Generic, Type, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis as AIORedis

class StressQuestionnaireAction:
    def __init__(
        self,
        sportsman_id: str,
        connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
        stress_questionnaire_id: str = "",
    ) -> None:
        self.connection_factory = connection_factory

        self.sportsman_id = sportsman_id
        self.stress_questionnaire_id = stress_questionnaire_id

        self.full_key = self._create_full_key(
            sportsman_id=sportsman_id,
            stress_questionnaire_id=stress_questionnaire_id,
        )
        self.sportsman_key_match = self._create_sportsman_key_match(
            sportsman_id=sportsman_id
        )

    def _create_full_key(self, sportsman_id: str, stress_questionnaire_id: str) -> str:
        return f"stress_questionnaire_{sportsman_id}_{stress_questionnaire_id}"

    def _create_sportsman_key_match(self, sportsman_id: str) -> str:
        return f"stress_questionnaire_{sportsman_id}_*"

    async def get_all_stress_qs(self) -> list[str]:
        async with self.connection_factory() as connection:
            all_qs_mathes = connection.scan_iter(self.sportsman_key_match)

        shift_len = len(self.sportsman_key_match) - 1
        questionnaire_ids = []
        async for qs_math in all_qs_mathes:
            questionnaire_ids.append(json.loads(qs_math)[shift_len:])

        return questionnaire_ids

    # async def set(self, new_action_data: BaseActionDataType) -> None:
    #     async with self.connection_factory() as connection:
    #         await connection.set(
    #             self.key, new_action_data.model_dump_json(), ex=self.timeout
    #         )

    # async def rmv(self) -> None:
    #     async with self.connection_factory() as connection:
    #         await connection.delete(self.key)

    # async def ttl(self) -> int:
    #     async with self.connection_factory() as connection:
    #         return int(await connection.ttl(self.key))
