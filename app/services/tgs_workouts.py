from uuid import UUID

from app import schemas
from app.models import TGSWorkouts
from app.repositories import TGSWorkoutsRepository


class TGSWorkoutsService:
    def __init__(self, repository: TGSWorkoutsRepository) -> None:
        self.repository = repository

    async def get_by_workout_id(self, workout_id: UUID) -> TGSWorkouts | None:
        return await self.repository.get_by_workout_id(workout_id=workout_id)

    async def create(self, schema_in: schemas.CreateTGSWorkoutIn) -> TGSWorkouts:
        return await self.repository.create(schema_in=schema_in)
