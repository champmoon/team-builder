from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TrainersWorkouts
from app.schemas import CreateTrainerWorkoutIn


class TrainersWorkoutsRepository:
    def __init__(
        self,
        model: Type[TrainersWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def create(self, schema_in: CreateTrainerWorkoutIn) -> TrainersWorkouts:
        async with self.session_factory() as session:
            created_Trainer_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_Trainer_workout.scalars().one()
    
