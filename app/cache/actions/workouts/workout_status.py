from contextlib import AbstractAsyncContextManager
from typing import Callable

from redis.asyncio import Redis as AIORedis

from app.consts import WorkoutsStatusesEnum


class WorkoutStatusAction:
    def __init__(
        self,
        workout_id: str,
        connection_factory: Callable[..., AbstractAsyncContextManager[AIORedis]],
        sportsman_id: str = "",
        trainer_id: str = "",
    ) -> None:
        self.connection_factory = connection_factory
        self.workout_id = workout_id
        self.sportsman_id = sportsman_id
        self.trainer_id = trainer_id

    @property
    def _planned_key(self) -> str:
        return f"{WorkoutsStatusesEnum.PLANNED.name}_workout_{self.workout_id}"

    @property
    def _skipped_sportsman_key(self) -> str:
        return (
            f"{WorkoutsStatusesEnum.SKIPPED.name}_workout"
            f"_{self.workout_id}_sportsman_{self.sportsman_id}"
        )

    @property
    def _skipped_trainer_key(self) -> str:
        return (
            f"{WorkoutsStatusesEnum.SKIPPED.name}_workout"
            f"_{self.workout_id}_trainer_{self.trainer_id}"
        )

    async def set_planned(self, timeout: int) -> None:
        async with self.connection_factory() as connection:
            await connection.set(
                self._planned_key,
                self._planned_key,
                ex=timeout,
            )

    async def is_planned(self) -> bool:
        async with self.connection_factory() as connection:
            getted_key = await connection.get(self._planned_key)

        return True if getted_key else False

    async def rmv_planned(self) -> None:
        async with self.connection_factory() as connection:
            await connection.delete(self._planned_key)

    async def begin_sportsman_skipped(self, timeout: int) -> None:
        async with self.connection_factory() as connection:
            await connection.set(
                self._skipped_sportsman_key,
                self._skipped_sportsman_key,
                ex=timeout,
            )

    async def is_sportsman_skipped(self) -> bool:
        async with self.connection_factory() as connection:
            getted_key = await connection.get(self._skipped_sportsman_key)

        return True if getted_key else False

    async def rmv_sportsman_skipped(self) -> None:
        async with self.connection_factory() as connection:
            await connection.delete(self._skipped_sportsman_key)

    async def begin_trainer_skipped(self, timeout: int) -> None:
        async with self.connection_factory() as connection:
            await connection.set(
                self._skipped_trainer_key,
                self._skipped_trainer_key,
                ex=timeout,
            )

    async def is_trainer_skipped(self) -> bool:
        async with self.connection_factory() as connection:
            getted_key = await connection.get(self._skipped_trainer_key)

        return True if getted_key else False

    async def rmv_trainer_skipped(self) -> None:
        async with self.connection_factory() as connection:
            await connection.delete(self._skipped_trainer_key)
