from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TeamsGroupsWorkouts
from app.schemas import CreateTeamGroupWorkoutIn


class TeamsGroupsWorkoutsRepository:
    def __init__(
        self,
        model: Type[TeamsGroupsWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_workout_id(self, workout_id: UUID) -> TeamsGroupsWorkouts | None:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()
    
    async def create(self, schema_in: CreateTeamGroupWorkoutIn) -> TeamsGroupsWorkouts:
        async with self.session_factory() as session:
            created_team_group_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_team_group_workout.scalars().one()
    
