from uuid import UUID

from app import schemas
from app.models.workouts import Workouts, WorkoutsPool
from app.repositories import WorkoutsRepository, WorkoutsPoolRepository


class WorkoutsService:
    def __init__(
        self,
        repository: WorkoutsRepository,
    ) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> Workouts | None:
        return await self.repository.get_by_id(id=id)

    async def create(self, schema_in: schemas.CreateWorkoutInDB) -> Workouts:
        return await self.repository.create(schema_in=schema_in)

    async def delete(self, id: UUID) -> Workouts:
        return await self.repository.delete(id=id)


class WorkoutsPoolService:
    def __init__(
        self,
        repository: WorkoutsPoolRepository,
    ) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> WorkoutsPool | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_trainer_id(self, trainer_id: UUID) -> WorkoutsPool | None:
        return await self.repository.get_by_trainer_id(trainer_id=trainer_id)

    async def create(self, schema_in: schemas.CreateWorkoutPoolInDB) -> WorkoutsPool:
        return await self.repository.create(schema_in=schema_in)

    async def update(
        self, id: UUID, schema_in: schemas.UpdateWorkoutPoolIn
    ) -> WorkoutsPool:
        return await self.repository.update(id=id, schema_in=schema_in)

    async def delete(self, id: UUID) -> WorkoutsPool:
        return await self.repository.delete(id=id)
