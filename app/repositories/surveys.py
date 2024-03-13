from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SportsmanSurveys, TeamSurveys


class TeamSurveysRepository:
    def __init__(
        self,
        model: Type[TeamSurveys],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_team_id(self, team_id: UUID) -> TeamSurveys | None:
        stmt = select(self.model).where(self.model.team_id == team_id)

        async with self.session_factory() as session:
            getted_teams = await session.execute(stmt)

        return getted_teams.scalars().first()

    async def create(
        self, team_id: UUID, main_fields: list[dict], add_fields: list[dict]
    ) -> TeamSurveys:
        async with self.session_factory() as session:
            created_team = await session.execute(
                insert(self.model)
                .values(team_id=team_id, main_fields=main_fields, add_fields=add_fields)
                .returning(self.model)
            )
            await session.commit()

        return created_team.scalars().one()

    async def update(self, id: UUID, add_fields: list[dict]) -> TeamSurveys:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(add_fields=add_fields)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_trainer = await session.execute(stmt)
            await session.commit()

        return updated_trainer.scalars().one()


class SportsmanSurveysRepository:
    def __init__(
        self,
        model: Type[SportsmanSurveys],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_sportsman_id(self, sportsman_id: UUID) -> SportsmanSurveys | None:
        stmt = select(self.model).where(self.model.sportsman_id == sportsman_id)

        async with self.session_factory() as session:
            getted_teams = await session.execute(stmt)

        return getted_teams.scalars().first()

    async def create(
        self, sportsman_id: UUID, team_survey_id: UUID
    ) -> SportsmanSurveys:
        async with self.session_factory() as session:
            created_team = await session.execute(
                insert(self.model)
                .values(
                    sportsman_id=sportsman_id,
                    team_survey_id=team_survey_id,
                    answers=[],
                )
                .returning(self.model)
            )
            await session.commit()

        return created_team.scalars().one()

    async def update(
        self, id: UUID, answers: list[dict], update_it: bool = False
    ) -> SportsmanSurveys:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(answers=answers, update_it=update_it)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_trainer = await session.execute(stmt)
            await session.commit()

        return updated_trainer.scalars().one()

    async def set_update(self, sportsman_id: UUID) -> SportsmanSurveys:
        stmt = (
            update(self.model)
            .where(self.model.sportsman_id == sportsman_id)
            .values(update_it=True)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_trainer = await session.execute(stmt)
            await session.commit()

        return updated_trainer.scalars().one()
