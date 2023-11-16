from uuid import UUID

from app import schemas
from app.models import TeamsGroupsWorkouts
from app.repositories import TeamsGroupsWorkoutsRepository
from app.utils import Hasher


class TeamsGroupsWorkoutsService:
    def __init__(self, repository: TeamsGroupsWorkoutsRepository) -> None:
        self.repository = repository

    async def get_by_workout_id(self, workout_id: UUID) -> TeamsGroupsWorkouts | None:
        return await self.repository.get_by_workout_id(workout_id=workout_id)

    async def create(
        self, schema_in: schemas.CreateTeamGroupWorkoutIn
    ) -> TeamsGroupsWorkouts:
        return await self.repository.create(schema_in=schema_in)
