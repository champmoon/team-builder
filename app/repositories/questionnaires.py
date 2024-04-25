from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from pydantic import NaiveDatetime
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.models import StressQuestionnaires


class StressQuestionnairesRepository:
    def __init__(
        self,
        model: Type[StressQuestionnaires],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> StressQuestionnaires | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_session = await session.execute(stmt)

        return getted_session.scalars().first()

    async def get_by_workout_id(self, workout_id: UUID) -> StressQuestionnaires | None:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted_session = await session.execute(stmt)

        return getted_session.scalars().first()

    async def get_by_ids(self, ids: list[UUID]) -> Sequence[StressQuestionnaires]:
        stmt = select(self.model).where(self.model.id.in_(ids))

        async with self.session_factory() as session:
            getted_session = await session.execute(stmt)

        return getted_session.scalars().all()

    async def get_all_by_sportsman_id(
        self,
        sportsman_id: UUID,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[StressQuestionnaires]:
        where_start_date: tuple = ()
        where_end_date: tuple = ()

        if start_date:
            where_start_date = (StressQuestionnaires.created_at >= start_date,)

        if end_date:
            where_end_date = (StressQuestionnaires.created_at <= end_date,)

        stmt = select(self.model).where(
            self.model.sportsman_id == sportsman_id,
            *where_start_date,
            *where_end_date,
        )

        async with self.session_factory() as session:
            getted_group = await session.execute(stmt)

        return getted_group.scalars().all()

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[StressQuestionnaires]:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted_group = await session.execute(stmt)

        return getted_group.scalars().all()

    async def create(
        self, schema_in: schemas.CreateStressQuestionnaireIn
    ) -> StressQuestionnaires:
        async with self.session_factory() as session:
            created_group = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_group.scalars().one()

    async def update(
        self, id: UUID, schema_in: schemas.UpdateStressQuestionnaireIn
    ) -> StressQuestionnaires:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_group = await session.execute(stmt)
            await session.commit()

        return updated_group.scalars().one()
