from uuid import UUID

from app import schemas
from app.models import Groups
from app.repositories import GroupsRepository


class GroupsService:
    def __init__(self, repository: GroupsRepository) -> None:
        self.repository = repository

    async def get_by_id(self, id: UUID) -> Groups | None:
        return await self.repository.get_by_id(id=id)

    async def get_all_by_trainer_id(self, trainer_id: UUID) -> Groups | None:
        return await self.repository.get_all_by_trainer_id(trainer_id=trainer_id)

    async def create(
        self, schema_in: schemas.CreateGroupIn, trainer_id: UUID
    ) -> Groups:
        return await self.repository.create(
            schema_in=schemas.CreateGroupInDB(
                trainer_id=trainer_id,
                name=schema_in.name,
            )
        )

    async def delete(self, id: UUID) -> Groups:
        return await self.repository.delete(id=id)
