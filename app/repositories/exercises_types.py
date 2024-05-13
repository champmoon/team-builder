from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.consts import ExercisesTypesEnum
from app.models import ExercisesTypes


class ExercisesTypesRepository:
    def __init__(
        self,
        model: Type[ExercisesTypes],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_type(
        self, type: ExercisesTypesEnum, trainer_id: UUID
    ) -> ExercisesTypes | None:
        stmt = select(self.model).where(
            self.model.type == type,
            self.model.trainer_id == trainer_id,
        )

        async with self.session_factory() as session:
            getted_exercises_type = await session.execute(stmt)

        return getted_exercises_type.scalars().first()

    async def get_all(self, trainer_id: UUID) -> Sequence[ExercisesTypes]:
        stmt = select(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            getted_exercises_types = await session.execute(stmt)

        return getted_exercises_types.scalars().all()

    async def create(
        self, schema_in: schemas.CreateExercisesTypeIn, trainer_id: UUID
    ) -> ExercisesTypes:
        async with self.session_factory() as session:
            created_exercises_type = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump(), trainer_id=trainer_id)
                .returning(self.model)
            )
            await session.commit()

        return created_exercises_type.scalars().one()

    async def update(
        self, schema_in: schemas.UpdateExercisesTypeIn, trainer_id: UUID
    ) -> ExercisesTypes:
        stmt = (
            update(self.model)
            .where(
                self.model.type == schema_in.type,
                self.model.trainer_id == trainer_id,
            )
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated = await session.execute(stmt)
            await session.commit()

        return updated.scalars().one()

    async def delete(
        self, type: ExercisesTypesEnum, trainer_id: UUID
    ) -> ExercisesTypes:
        stmt = (
            delete(self.model)
            .where(self.model.type == type, self.model.trainer_id == trainer_id)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            deleted = await session.execute(stmt)
            await session.commit()

        return deleted.scalars().one()

    async def delete_by_trainer_id(self, trainer_id: UUID) -> None:
        stmt = delete(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            await session.execute(stmt)
            await session.commit()
