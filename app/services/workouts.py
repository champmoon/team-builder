from uuid import UUID

from sqlalchemy import select
from app import schemas
from app.models.exercises import Exercises
from app.models.workouts import Workouts
from app.repositories import WorkoutsRepository
from app import consts
from .exercises import ExercisesService
from .sportsmans_workouts import SportsmansWorkoutsService
from .trainers_workouts import TrainersWorkoutsService
from .workouts_statuses import WorkoutsStatusesService
from .exercises_types import ExercisesTypesService


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

    async def update(self, id: UUID, schema_in: schemas.UpdateWorkoutIn) -> Workouts:
        return await self.repository.update(id=id, schema_in=schema_in)

    async def delete(self, id: UUID) -> Workouts:
        return await self.repository.delete(id=id)
