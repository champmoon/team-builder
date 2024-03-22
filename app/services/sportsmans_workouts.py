from typing import Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
from app.models import SportsmansWorkouts
from app.repositories import SportsmansWorkoutsRepository


class SportsmansWorkoutsService:
    def __init__(self, repository: SportsmansWorkoutsRepository) -> None:
        self.repository = repository

    async def get_all_by_sportsman_id(
        self,
        sportsman_id: UUID,
        offset: int = 0,
        limit: int = 100,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_all_by_sportsman_id(
            sportsman_id=sportsman_id,
            offset=offset,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_all_by_workout_id(workout_id=workout_id)

    async def get_by(
        self, workout_id: UUID, sportsman_id: UUID
    ) -> SportsmansWorkouts | None:
        return await self.repository.get_by(
            workout_id=workout_id, sportsman_id=sportsman_id
        )

    async def create(
        self, schema_in: schemas.CreateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        return await self.repository.create(schema_in=schema_in)
