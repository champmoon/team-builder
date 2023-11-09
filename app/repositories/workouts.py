from contextlib import AbstractAsyncContextManager
from typing import Callable, Type

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import Workouts


class WorkoutsRepository:
    def __init__(
        self,
        model: Type[Workouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def create(self, schema_in: schemas.CreateWorkoutInDB) -> Workouts:
        async with self.session_factory() as session:
            created_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_workout.scalars().one()
