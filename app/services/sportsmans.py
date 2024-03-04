from typing import Sequence
from uuid import UUID

from app import schemas
from app.models import Sportsmans
from app.repositories import SportsmansRepository
from app.utils import Hasher


class SportsmansService:
    def __init__(self, repository: SportsmansRepository) -> None:
        self.repository = repository

    async def get_by_email(self, email: str) -> Sportsmans | None:
        return await self.repository.get_by_email(email=email)

    async def get_by_id(self, id: UUID) -> Sportsmans | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_team_id(self, team_id: UUID) -> Sequence[Sportsmans]:
        return await self.repository.get_by_team_id(team_id=team_id)

    async def create(self, schema_in: schemas.CreateSportsmanIn) -> Sportsmans:
        return await self.repository.create(
            schema_in=schemas.CreateSportsmanInDB(
                email=schema_in.email,
                hashed_password=Hasher(secret=schema_in.password).hash(),
                team_id=schema_in.team_id,
                first_name=schema_in.first_name,
                middle_name=schema_in.middle_name,
                last_name=schema_in.last_name,
            )
        )

    async def update(
        self, id: UUID, schema_in: schemas.UpdateSportsmanIn
    ) -> Sportsmans:
        return await self.repository.update(id=id, schema_in=schema_in)

    async def add_to_team(self, sportsman_id: UUID, team_id: UUID) -> Sportsmans:
        return await self.repository.add_to_team(id=sportsman_id, team_id=team_id)

    async def kick_off_team(self, sportsman_id: UUID) -> Sportsmans:
        return await self.repository.kick_off_team(id=sportsman_id)
