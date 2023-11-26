from app import schemas
from app.models import SportsmansWorkouts
from app.repositories import SportsmansWorkoutsRepository


class SportsmansWorkoutsService:
    def __init__(self, repository: SportsmansWorkoutsRepository) -> None:
        self.repository = repository

    async def create(
        self, schema_in: schemas.CreateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        return await self.repository.create(schema_in=schema_in)
