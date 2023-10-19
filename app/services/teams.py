from uuid import UUID

from app import schemas
from app.models import Teams
from app.repositories import TeamsRepository


class TeamsService:
    def __init__(self, repository: TeamsRepository) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> Teams | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_trainer_id(self, trainer_id: UUID) -> Teams | None:
        return await self.repository.get_by_trainer_id(trainer_id=trainer_id)

    async def create(self, schema_in: schemas.CreateTeamIn) -> Teams:
        return await self.repository.create(schema_in=schema_in)
