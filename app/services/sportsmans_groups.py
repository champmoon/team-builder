from typing import Sequence
from uuid import UUID

from app import schemas
from app.models import SportsmansGroups
from app.repositories import SportsmansGroupsRepository


class SportsmansGroupsService:
    def __init__(self, repository: SportsmansGroupsRepository) -> None:
        self.repository = repository

    async def get_by(
        self, sportsman_id: UUID, group_id: UUID
    ) -> SportsmansGroups | None:
        return await self.repository.get_by(
            sportsman_id=sportsman_id, group_id=group_id
        )

    async def get_all_groups_by_sportsman_id(
        self, sportsman_id: UUID
    ) -> Sequence[SportsmansGroups]:
        return await self.repository.get_all_groups_by_sportsman_id(
            sportsman_id=sportsman_id
        )

    async def get_all_sportsmans_by_group_id(
        self, group_id: UUID
    ) -> Sequence[SportsmansGroups]:
        return await self.repository.get_all_sportsmans_by_group_id(group_id=group_id)

    async def create(
        self, schema_in: schemas.CreateSportsmanGroupIn
    ) -> SportsmansGroups:
        return await self.repository.create(schema_in=schema_in)

    async def delete(
        self, schema_in: schemas.DeleteSportsmanGroupIn
    ) -> SportsmansGroups:
        return await self.repository.delete(schema_in=schema_in)

    async def merge(
        self,
        local_sportsman_id: UUID,
        true_sportsman_id: UUID,
    ) -> None:
        return await self.repository.merge(
            local_sportsman_id=local_sportsman_id,
            true_sportsman_id=true_sportsman_id,
        )
