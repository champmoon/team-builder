from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Teams
from app.schemas.teams import CreateTeamIn


class TeamsRepository:
    def __init__(
        self,
        model: Type[Teams],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Teams | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_team = await session.execute(stmt)

        return getted_team.scalars().first()

    async def get_by_trainer_id(self, trainer_id: UUID) -> Teams | None:
        stmt = select(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            getted_team = await session.execute(stmt)

        return getted_team.scalars().first()

    async def get_all(self) -> Sequence[Teams]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_teams = await session.execute(stmt)

        return getted_teams.scalars().all()

    async def create(self, schema_in: CreateTeamIn) -> Teams:
        async with self.session_factory() as session:
            created_team = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_team.scalars().one()

    async def delete(self, id: UUID) -> Teams:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_team = await session.execute(stmt)
            await session.commit()

        return deleted_team.scalars().one()
