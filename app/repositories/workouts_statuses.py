from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import WorkoutsStatusesEnum
from app.models import WorkoutsStatuses
from app.schemas import CreateWorkoutStatusesIn


class WorkoutsStatusesRepository:
    def __init__(
        self,
        model: Type[WorkoutsStatuses],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_status(
        self, status: WorkoutsStatusesEnum
    ) -> WorkoutsStatuses | None:
        stmt = select(self.model).where(self.model.status == status)

        async with self.session_factory() as session:
            getted_workout_status = await session.execute(stmt)

        return getted_workout_status.scalars().first()

    async def get_all(self) -> Sequence[WorkoutsStatuses]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_workouts_statuses = await session.execute(stmt)

        return getted_workouts_statuses.scalars().all()

    async def create(self, schema_in: CreateWorkoutStatusesIn) -> WorkoutsStatuses:
        async with self.session_factory() as session:
            created_workout_status = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_workout_status.scalars().one()
