from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TGSWorkouts
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

    async def create(self, schema_in: CreateTGSWorkoutIn) -> TGSWorkouts:
        async with self.session_factory() as session:
            created_tgs_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_tgs_workout.scalars().one()
