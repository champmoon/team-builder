from contextlib import AbstractAsyncContextManager
from typing import Callable, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import Workouts, WorkoutsPool


class WorkoutsRepository:
    def __init__(
        self,
        model: Type[Workouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Workouts | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def create(self, schema_in: schemas.CreateWorkoutInDB) -> Workouts:
        async with self.session_factory() as session:
            created_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_workout.scalars().one()

    async def delete(self, id: UUID) -> Workouts:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_workout = await session.execute(stmt)
            await session.commit()

        return deleted_workout.scalars().one()


class WorkoutsPoolRepository:
    def __init__(
        self,
        model: Type[WorkoutsPool],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_trainer_id(self, trainer_id: UUID) -> WorkoutsPool | None:
        stmt = select(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def get_by_id(self, id: UUID) -> WorkoutsPool | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def create(self, schema_in: schemas.CreateWorkoutPoolInDB) -> WorkoutsPool:
        async with self.session_factory() as session:
            created_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_workout.scalars().one()

    async def update(
        self, id: UUID, schema_in: schemas.UpdateWorkoutPoolIn
    ) -> WorkoutsPool:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_workout = await session.execute(stmt)
            await session.commit()

        return updated_workout.scalars().one()

    async def delete(self, id: UUID) -> WorkoutsPool:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_workout = await session.execute(stmt)
            await session.commit()

        return deleted_workout.scalars().one()
