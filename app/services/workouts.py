import datetime
from typing import Callable, Sequence
from uuid import UUID

from app import schemas
from app.cache import actions as acts
from app.models.workouts import Workouts, WorkoutsPool
from app.repositories import WorkoutsPoolRepository, WorkoutsRepository


class WorkoutsService:
    def __init__(
        self,
        repository: WorkoutsRepository,
        workouts_status_action_part: Callable[
            [str, str | None], acts.Actions.workouts_status
        ],
    ) -> None:
        self.repository = repository
        self.workouts_status_action_part = workouts_status_action_part

    async def get_by_id(self, id: UUID) -> Workouts | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_pool_id(self, pool_id: UUID) -> Sequence[Workouts]:
        return await self.repository.get_by_pool_id(pool_id=pool_id)

    async def create(self, schema_in: schemas.CreateWorkoutInDB) -> Workouts:
        new_workout_out = await self.repository.create(schema_in=schema_in)

        now_time = datetime.datetime.now() + datetime.timedelta(hours=3)

        exp_time = round((new_workout_out.date - now_time).total_seconds())
        if exp_time < 0:
            return new_workout_out

        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(new_workout_out.id)  # type: ignore
        )
        await workouts_status_action.set_planned(timeout=exp_time)

        return new_workout_out

    async def start(self, workout_id: UUID) -> None:
        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(workout_id)  # type: ignore
        )
        await workouts_status_action.rmv_planned()

    async def is_planned(self, workout_id: UUID) -> bool:
        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(workout_id)  # type: ignore
        )
        return await workouts_status_action.is_planned()

    async def set_unvisible(self, id: UUID) -> Workouts:
        return await self.repository.set_unvisible(id=id)

    async def delete(self, id: UUID) -> Workouts:
        return await self.repository.delete(id=id)

    async def delete_many(self, ids: Sequence[UUID]) -> None:
        return await self.repository.delete_many(ids=ids)

    async def update(self, id: UUID, schema_in: schemas.UpdateWorkoutIn) -> Workouts:
        return await self.repository.update(id=id, schema_in=schema_in)

    async def reassign(self, id: UUID, workout_pool_id: UUID) -> Workouts:
        return await self.repository.reassign(id=id, workout_pool_id=workout_pool_id)


class WorkoutsPoolService:
    def __init__(
        self,
        repository: WorkoutsPoolRepository,
    ) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> WorkoutsPool | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_trainer_id(self, trainer_id: UUID) -> Sequence[WorkoutsPool]:
        return await self.repository.get_by_trainer_id(trainer_id=trainer_id)

    async def create(self, schema_in: schemas.CreateWorkoutPoolInDB) -> WorkoutsPool:
        return await self.repository.create(schema_in=schema_in)

    async def update(
        self, id: UUID, schema_in: schemas.UpdateWorkoutPoolIn
    ) -> WorkoutsPool:
        return await self.repository.update(id=id, schema_in=schema_in)

    async def set_unvisible(self, id: UUID) -> WorkoutsPool:
        return await self.repository.set_unvisible(id=id)

    async def delete(self, id: UUID) -> WorkoutsPool:
        return await self.repository.delete(id=id)
