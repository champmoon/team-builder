from uuid import UUID

from app import schemas
from app.models import Admins
from app.repositories import AdminsRepository
from app.utils import Hasher


class AdminsService:
    def __init__(self, repository: AdminsRepository) -> None:
        self.repository = repository

    async def get_by_email(self, email: str) -> Admins | None:
        return await self.repository.get_by_email(email=email)

    async def get_by_id(self, id: UUID) -> Admins | None:
        return await self.repository.get_by_id(id=id)

    async def create(self, schema_in: schemas.CreateAdminIn) -> Admins:
        return await self.repository.create(
            schema_in=schemas.CreateAdminInDB(
                email=schema_in.email,
                hashed_password=Hasher(secret=schema_in.password).hash(),
            )
        )
