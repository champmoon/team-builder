from uuid import UUID

from app import schemas
from app.models import Trainers
from app.repositories import TrainersRepository
from app.utils import Hasher


class TrainersService:
    def __init__(self, repository: TrainersRepository) -> None:
        self.repository = repository

    async def get_by_email(self, email: str) -> Trainers | None:
        return await self.repository.get_by_email(email=email)

    async def get_by_id(self, id: UUID) -> Trainers | None:
        return await self.repository.get_by_id(id=id)

    async def create(self, schema_in: schemas.CreateTrainerIn) -> Trainers:
        return await self.repository.create(
            schema_in=schemas.CreateTrainerInDB(
                email=schema_in.email,
                hashed_password=Hasher(secret=schema_in.password).hash(),
                name=schema_in.name,
            )
        )

    async def update(self, id: UUID, schema_in: schemas.UpdateTrainerIn) -> Trainers:
        return await self.repository.update(id=id, schema_in=schema_in)
