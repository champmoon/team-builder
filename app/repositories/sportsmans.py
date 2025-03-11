from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Sportsmans
from app.schemas.sportsmans import (
    CreateSportsmanInDB,
    InnerUpdateSportsmanPasswordIn,
    UpdateSportsmanIn,
)


class SportsmansRepository:
    def __init__(
        self,
        model: Type[Sportsmans],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Sportsmans | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_sportsman = await session.execute(stmt)

        return getted_sportsman.scalars().first()

    async def get_by_email(self, email: str) -> Sportsmans | None:
        stmt = select(self.model).where(self.model.email == email)

        async with self.session_factory() as session:
            getted_sportsman = await session.execute(stmt)

        return getted_sportsman.scalars().first()

    async def get_by_team_id(self, team_id: UUID) -> Sequence[Sportsmans]:
        stmt = select(self.model).where(self.model.team_id == team_id)

        async with self.session_factory() as session:
            getted_sportsman = await session.execute(stmt)

        return getted_sportsman.scalars().all()

    async def get_all(self) -> Sequence[Sportsmans]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_sportsmans = await session.execute(stmt)

        return getted_sportsmans.scalars().all()

    async def create(self, schema_in: CreateSportsmanInDB) -> Sportsmans:
        async with self.session_factory() as session:
            created_sportsman = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_sportsman.scalars().one()

    async def update(
        self, id: UUID, schema_in: UpdateSportsmanIn | InnerUpdateSportsmanPasswordIn
    ) -> Sportsmans:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_sportsman = await session.execute(stmt)
            await session.commit()

        return updated_sportsman.scalars().one()

    async def update_avatar(self, id: UUID, avatar_uri: str) -> Sportsmans:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(avatar_uri=avatar_uri)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_sportsman = await session.execute(stmt)
            await session.commit()

        return updated_sportsman.scalars().one()

    async def delete(self, id: UUID) -> Sportsmans:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_sportsman = await session.execute(stmt)
            await session.commit()

        return deleted_sportsman.scalars().one()

    async def add_to_team(self, id: UUID, team_id: UUID) -> Sportsmans:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(team_id=team_id)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_sportsman = await session.execute(stmt)
            await session.commit()

        return updated_sportsman.scalars().one()

    async def kick_off_team(self, id: UUID) -> Sportsmans:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(team_id=None)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_sportsman = await session.execute(stmt)
            await session.commit()

        return updated_sportsman.scalars().one()
