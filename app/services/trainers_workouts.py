from typing import Sequence
from uuid import UUID

from app import schemas
from app.models import TrainersWorkouts
from app.repositories import TrainersWorkoutsRepository


class TrainersWorkoutsService:
    def __init__(self, repository: TrainersWorkoutsRepository) -> None:
        self.repository = repository

    async def get_all_by_trainer_id(
        self, trainer_id: UUID
    ) -> Sequence[TrainersWorkouts]:
        return await self.repository.get_all_by_trainer_id(trainer_id=trainer_id)

    async def get_by_workout_id(self, workout_id: UUID) -> TrainersWorkouts | None:
        return await self.repository.get_by_workout_id(workout_id=workout_id)

    async def create(
        self, schema_in: schemas.CreateTrainerWorkoutIn
    ) -> TrainersWorkouts:
        return await self.repository.create(schema_in=schema_in)
