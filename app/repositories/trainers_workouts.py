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

    async def get_all_by_trainer_id(self, trainer_id: UUID) -> Sequence[TrainersWorkouts]:
        stmt = select(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()
    
    async def create(self, schema_in: CreateTrainerWorkoutIn) -> TrainersWorkouts:
        async with self.session_factory() as session:
            created_trainer_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_trainer_workout.scalars().one()
    
