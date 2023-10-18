from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sessions import Sessions
from app.schemas.sessions import CreateSessionIn


class SessionsRepository:
    def __init__(
        self,
        model: Type[Sessions],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_user_id(self, user_id: UUID) -> Sessions | None:
        stmt = select(self.model).where(self.model.user_id == user_id)

        async with self.session_factory() as session:
            getted_session = await session.execute(stmt)

        return getted_session.scalars().first()

    async def get_by_refresh_token(self, refresh_token: UUID) -> Sessions | None:
        stmt = select(self.model).where(self.model.refresh_token == refresh_token)

        async with self.session_factory() as session:
            getted_session = await session.execute(stmt)

        return getted_session.scalars().first()

    async def create(self, schema_in: CreateSessionIn) -> Sessions:
        async with self.session_factory() as session:
            created_session = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_session.scalars().one()

    async def delete_by_user_id(self, user_id: UUID) -> None:
        stmt = delete(self.model).where(self.model.user_id == user_id)

        async with self.session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    async def delete_by_refresh_token(self, refresh_token: UUID) -> None:
        stmt = delete(self.model).where(self.model.refresh_token == refresh_token)

        async with self.session_factory() as session:
            await session.execute(stmt)
            await session.commit()
