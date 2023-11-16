from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import Exercises


class ExercisesRepository:
    def __init__(
        self,
        model: Type[Exercises],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_all_exercises_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[Exercises]:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted_exercises = await session.execute(stmt)

        return getted_exercises.scalars().all()
    
    async def create(self, schema_in: schemas.CreateExerciseInDB) -> Exercises:
        async with self.session_factory() as session:
            created_exercise = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_exercise.scalars().one()
