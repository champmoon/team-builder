from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TeamSurveys
from app.schemas.teams import CreateTeamIn


class TeamSurveysRepository:
    def __init__(
        self,
        model: Type[TeamSurveys],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_all(self) -> Sequence[TeamSurveys]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_teams = await session.execute(stmt)

        return getted_teams.scalars().all()

    async def create(self, team_id: UUID, main_fields: dict) -> TeamSurveys:
        async with self.session_factory() as session:
            created_team = await session.execute(
                insert(self.model)
                .values(team_id=team_id, main_fields=main_fields)
                .returning(self.model)
            )
            await session.commit()

        return created_team.scalars().one()
