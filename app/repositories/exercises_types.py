from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import ExercisesTypesEnum
from app.models import ExercisesTypes
from app.schemas import CreateExercisesTypeIn


class ExercisesTypesRepository:
    def __init__(
        self,
        model: Type[ExercisesTypes],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_type(self, type: ExercisesTypesEnum) -> ExercisesTypes | None:
        stmt = select(self.model).where(self.model.type == type)

        async with self.session_factory() as session:
            getted_exercises_type = await session.execute(stmt)

        return getted_exercises_type.scalars().first()

    async def get_all(self) -> Sequence[ExercisesTypes]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_exercises_types = await session.execute(stmt)

        return getted_exercises_types.scalars().all()

    async def create(self, schema_in: CreateExercisesTypeIn) -> ExercisesTypes:
        async with self.session_factory() as session:
            created_group = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_group.scalars().one()
