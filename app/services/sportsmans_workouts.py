from typing import Sequence
from uuid import UUID

from app import schemas
from app.models import SportsmansWorkouts
from app.repositories import SportsmansWorkoutsRepository


class SportsmansWorkoutsService:
    def __init__(self, repository: SportsmansWorkoutsRepository) -> None:
        self.repository = repository

    async def get_all_by_sportsman_id(
        self, sportsman_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_all_by_sportsman_id(sportsman_id=sportsman_id)

    async def create(
        self, schema_in: schemas.CreateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        return await self.repository.create(schema_in=schema_in)
