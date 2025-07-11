from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from pydantic import NaiveDatetime
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SportsmansWorkouts
from app.schemas.sportsmans_workouts import (
    CreateSportsmansWorkoutIn,
)

from .workouts import Workouts


class SportsmansWorkoutsRepository:
    def __init__(
        self,
        model: Type[SportsmansWorkouts],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_all_by_sportsman_id(
        self,
        sportsman_id: UUID,
        offset: int = 0,
        limit: int = 100,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[SportsmansWorkouts]:
        where_start_date: tuple = ()
        where_end_date: tuple = ()

        if start_date:
            where_start_date = (Workouts.date >= start_date,)

        if end_date:
            where_end_date = (Workouts.date <= end_date,)

        stmt = (
            select(self.model)
            .join(Workouts, self.model.workout_id == Workouts.id)
            .where(
                self.model.sportsman_id == sportsman_id,
                *where_start_date,
                *where_end_date,
            )
            .order_by(Workouts.date)
        )

        stmt = stmt.offset(offset).limit(limit)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        stmt = select(self.model).where(self.model.workout_id == workout_id)

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().all()

    async def get_by(
        self, workout_id: UUID, sportsman_id: UUID
    ) -> SportsmansWorkouts | None:
        stmt = select(self.model).where(
            self.model.workout_id == workout_id,
            self.model.sportsman_id == sportsman_id,
        )

        async with self.session_factory() as session:
            getted = await session.execute(stmt)

        return getted.scalars().first()

    async def create(self, schema_in: CreateSportsmansWorkoutIn) -> SportsmansWorkouts:
        async with self.session_factory() as session:
            created_sportsman_workout = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_sportsman_workout.scalars().one()

    async def update(
        self,
        ids: list[UUID],
        is_attend: bool | None = None,
        is_paid: bool | None = None,
    ) -> Sequence[SportsmansWorkouts]:
        if isinstance(is_attend, bool):
            stmt = (
                update(self.model)
                .where(self.model.sportsman_id.in_(ids))
                .values(is_attend=is_attend)
                .returning(self.model)
            )
        elif isinstance(is_paid, bool):
            stmt = (
                update(self.model)
                .where(self.model.sportsman_id.in_(ids))
                .values(is_paid=is_paid)
                .returning(self.model)
            )
        else:
            raise ValueError

        async with self.session_factory() as session:
            updated_workout = await session.execute(stmt)
            await session.commit()

        return updated_workout.scalars().all()

    # async def update_status(
    #     self, schema_in: UpdateSportsmansWorkoutIn, status_id: UUID
    # ) -> SportsmansWorkouts:
    #     stmt = (
    #         update(self.model)
    #         .where(
    #             self.model.sportsman_id == schema_in.sportsman_id,
    #             self.model.workout_id == schema_in.workout_id,
    #         )
    #         .values(status_id=status_id)
    #         .returning(self.model)
    #     )

    #     async with self.session_factory() as session:
    #         updated_sportsman = await session.execute(stmt)
    #         await session.commit()

    #     return updated_sportsman.scalars().one()

    async def bind_sportsman_to_workouts(
        self,
        sportsman_id: UUID,
        workouts_ids: Sequence[UUID],
    ) -> None:
        if len(workouts_ids) == 0:
            return

        async with self.session_factory() as session:
            await session.execute(
                insert(self.model).values(
                    [
                        {
                            "workout_id": workout_id,
                            "sportsman_id": sportsman_id,
                        }
                        for workout_id in workouts_ids
                    ]
                )
            )
            await session.commit()

    async def unbind_sportsman_to_workouts(
        self, sportsman_id: UUID, workouts_ids: Sequence[UUID]
    ) -> None:
        if len(workouts_ids) == 0:
            return

        async with self.session_factory() as session:
            await session.execute(
                delete(self.model).where(
                    self.model.sportsman_id == sportsman_id,
                    self.model.workout_id.in_(workouts_ids),
                )
            )
            await session.commit()

    # async def get_other_by_statuses(
    #     self,
    #     workout_id: UUID,
    #     self_sportsman_id: UUID,
    #     statuses: tuple[WorkoutsStatusesEnum, ...],
    # ) -> Sequence[SportsmansWorkouts]:
    #     stmt = (
    #         select(self.model)
    #         .join(WorkoutsStatuses, WorkoutsStatuses.id == self.model.status_id)
    #         .where(
    #             self.model.workout_id == workout_id,
    #             self.model.sportsman_id != self_sportsman_id,
    #             WorkoutsStatuses.status.in_(statuses),
    #         )
    #     )
    #     async with self.session_factory() as session:
    #         getted = await session.execute(stmt)

    #     return getted.scalars().all()

    async def merge(self, local_sportsman_id: UUID, true_sportsman_id: UUID) -> None:
        stmt = (
            update(self.model)
            .where(self.model.sportsman_id == local_sportsman_id)
            .values(sportsman_id=true_sportsman_id)
        )

        async with self.session_factory() as session:
            await session.execute(stmt)
            await session.commit()
