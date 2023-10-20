from app import schemas
from app.models import SportsmansGroups
from app.repositories import SportsmansGroupsRepository


class SportsmansGroupsService:
    def __init__(self, repository: SportsmansGroupsRepository) -> None:
        self.repository = repository

    async def create(
        self, schema_in: schemas.CreateSportsmanGroupIn
    ) -> SportsmansGroups:
        return await self.repository.create(schema_in=schema_in)

    async def delete(
        self, schema_in: schemas.DeleteSportsmanGroupIn
    ) -> SportsmansGroups:
        return await self.repository.delete(schema_in=schema_in)
