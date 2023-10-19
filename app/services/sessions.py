from datetime import datetime, timedelta
from uuid import UUID, uuid4

from app.conf.settings import settings
from app.consts import UsersTypes
from app.models import Sessions
from app.repositories import SessionsRepository
from app.schemas import CreateSessionIn


class SessionsService:
    def __init__(self, repository: SessionsRepository) -> None:
        self.repository = repository

    async def get_by_refresh_token(self, refresh_token: UUID) -> Sessions | None:
        return await self.repository.get_by_refresh_token(refresh_token=refresh_token)

    async def create(self, user_id: UUID, user_type: UsersTypes) -> Sessions:
        create_session_in = CreateSessionIn(
            user_id=user_id,
            refresh_token=uuid4(),
            user_type=user_type,
        )
        return await self.repository.create(schema_in=create_session_in)

    async def delete_all_by_user_id(self, user_id: UUID) -> None:
        return await self.repository.delete_by_user_id(user_id=user_id)

    async def delete_by_refresh_token(self, refresh_token: UUID) -> None:
        return await self.repository.delete_by_refresh_token(
            refresh_token=refresh_token
        )

    def is_refresh_token_expired(self, created_at: datetime) -> bool:
        return (
            created_at + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        ) <= datetime.utcnow()
