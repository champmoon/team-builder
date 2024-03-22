from typing import Sequence
from uuid import UUID

from app import schemas
from app.models.workouts import Workouts, WorkoutsPool
from app.repositories import WorkoutsPoolRepository, WorkoutsRepository


class WorkoutsService:
    def __init__(
        self,
        repository: WorkoutsRepository,
    ) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> Workouts | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_pool_id(self, pool_id: UUID) -> Sequence[Workouts]:
        return await self.repository.get_by_pool_id(pool_id=pool_id)

    async def create(self, schema_in: schemas.CreateWorkoutInDB) -> Workouts:
        return await self.repository.create(schema_in=schema_in)

    async def set_unvisible(self, id: UUID) -> Workouts:
        return await self.repository.set_unvisible(id=id)

    async def delete(self, id: UUID) -> Workouts:
        return await self.repository.delete(id=id)

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
