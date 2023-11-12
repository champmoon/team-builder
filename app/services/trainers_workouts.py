from uuid import UUID

from app import schemas
from app.models import TrainersWorkouts
from app.repositories import TrainersWorkoutsRepository
from app.utils import Hasher


class TrainersWorkoutsService:
    def __init__(self, repository: TrainersWorkoutsRepository) -> None:
        self.repository = repository

    async def create(
        self, schema_in: schemas.CreateTrainerWorkoutIn
    ) -> TrainersWorkouts:
        return await self.repository.create(schema_in=schema_in)
