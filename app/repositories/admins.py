from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admins import Admins
from app.schemas.admins import CreateAdminInDB


class AdminsRepository:
    def __init__(
        self,
        model: Type[Admins],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Admins | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_admin = await session.execute(stmt)

        return getted_admin.scalars().first()

    async def get_by_email(self, email: str) -> Admins | None:
        stmt = select(self.model).where(self.model.email == email)

        async with self.session_factory() as session:
            getted_admin = await session.execute(stmt)

        return getted_admin.scalars().first()

    async def get_all(self) -> Sequence[Admins]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_admins = await session.execute(stmt)

        return getted_admins.scalars().all()

    async def create(self, schema_in: CreateAdminInDB) -> Admins:
        async with self.session_factory() as session:
            created_admin = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_admin.scalars().one()
