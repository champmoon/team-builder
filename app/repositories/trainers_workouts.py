from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from pydantic import NaiveDatetime
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TrainersWorkouts
from app.schemas import CreateTrainerWorkoutIn, UpdateTrainerWorkoutIn

from .workouts import Workouts


class TrainersWorkoutsRepository:
    def __init__(
        self,
        model: Type[TrainersWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_all_by_trainer_id(
        self,
        trainer_id: UUID,
        offset: int = 0,
        limit: int = 100,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[TrainersWorkouts]:
        where_start_date: tuple = ()
        where_end_date: tuple = ()

        if start_date:
            where_start_date = (Workouts.date >= start_date,)

        if end_date:
            where_end_date = (Workouts.date <= end_date,)

        stmt = (
            select(self.model)
            .join(Workouts, self.model.workout_id == Workouts.id)
            .where(
                self.model.trainer_id == trainer_id,
                *where_start_date,
                *where_end_date,
            )
            .order_by(Workouts.date)
        )

        stmt = stmt.offset(offset).limit(limit)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[TrainersWorkouts]:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_by(
        self, workout_id: UUID, trainer_id: UUID
    ) -> TrainersWorkouts | None:
        stmt = select(self.model).where(
            self.model.workout_id == workout_id,
            self.model.trainer_id == trainer_id,
        )

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def create(
        self, schema_in: CreateTrainerWorkoutIn, status_id: UUID
    ) -> TrainersWorkouts:
        async with self.session_factory() as session:
            created_trainer_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump(), status_id=status_id)
                .returning(self.model)
            )
            await session.commit()

        return created_trainer_workout.scalars().one()

    async def update_status(
        self, schema_in: UpdateTrainerWorkoutIn, status_id: UUID
    ) -> TrainersWorkouts:
        stmt = (
            update(self.model)
            .where(
                self.model.trainer_id == schema_in.trainer_id,
                self.model.workout_id == schema_in.workout_id,
            )
            .values(status_id=status_id)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_sportsman = await session.execute(stmt)
            await session.commit()

        return updated_sportsman.scalars().one()
