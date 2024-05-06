import datetime
from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TGSWorkouts, Workouts
from app.schemas import CreateTGSWorkoutIn


class TGSWorkoutsRepository:
    def __init__(
        self,
        model: Type[TGSWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_workout_id(self, workout_id: UUID) -> TGSWorkouts | None:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def get_all_by_sportsman_id(
        self, sportsman_id: UUID
    ) -> Sequence[TGSWorkouts]:
        stmt = select(self.model).where(self.model.sportsman_id == sportsman_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_all_by_group_id(self, group_id: UUID) -> Sequence[TGSWorkouts]:
        stmt = select(self.model).where(self.model.group_id == group_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_all_by_team_id(self, team_id: UUID) -> Sequence[TGSWorkouts]:
        stmt = select(self.model).where(self.model.team_id == team_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def create(self, schema_in: CreateTGSWorkoutIn) -> TGSWorkouts:
        async with self.session_factory() as session:
            created_tgs_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_tgs_workout.scalars().one()

    async def delete(self, id: UUID) -> TGSWorkouts:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_workout = await session.execute(stmt)
            await session.commit()

        return deleted_workout.scalars().one()

    async def get_future_group_workouts_ids(self, group_id: UUID) -> Sequence[UUID]:
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        stmt = (
            select(self.model.workout_id)
            .join(Workouts, self.model.workout_id == Workouts.id)
            .where(
                self.model.group_id == group_id,
                Workouts.date > now,
            )
        )
        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_future_team_workouts_ids(self, team_id: UUID) -> Sequence[UUID]:
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        stmt = (
            select(self.model.workout_id)
            .join(Workouts, self.model.workout_id == Workouts.id)
            .where(
                self.model.team_id == team_id,
                Workouts.date > now,
            )
        )
        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()
