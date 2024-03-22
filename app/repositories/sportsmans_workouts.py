from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SportsmansWorkouts
from app.schemas.sportsmans_workouts import CreateSportsmansWorkoutIn


class SportsmansWorkoutsRepository:
    def __init__(
        self,
        model: Type[SportsmansWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_all_by_sportsman_id(
        self, sportsman_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        stmt = select(self.model).where(self.model.sportsman_id == sportsman_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def create(self, schema_in: CreateSportsmansWorkoutIn) -> SportsmansWorkouts:
        async with self.session_factory() as session:
            created_sportsman_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_sportsman_workout.scalars().one()
