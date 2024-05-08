import datetime
from typing import Callable, Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
from app.cache import actions as acts
from app.consts import WorkoutsStatusesEnum
from app.models import SportsmansWorkouts
from app.repositories import SportsmansWorkoutsRepository, WorkoutsStatusesRepository


class SportsmansWorkoutsService:
    def __init__(
        self,
        repository: SportsmansWorkoutsRepository,
        statuses_repository: WorkoutsStatusesRepository,
        workouts_status_action_part: Callable[
            [str, str | None], acts.Actions.workouts_status
        ],
    ) -> None:
        self.repository = repository
        self.statuses_repository = statuses_repository
        self.workouts_status_action_part = workouts_status_action_part

    async def get_all_by_sportsman_id(
        self,
        sportsman_id: UUID,
        offset: int = 0,
        limit: int = 100,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_all_by_sportsman_id(
            sportsman_id=sportsman_id,
            offset=offset,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_all_by_workout_id(workout_id=workout_id)

    async def get_by(
        self, workout_id: UUID, sportsman_id: UUID
    ) -> SportsmansWorkouts | None:
        return await self.repository.get_by(
            workout_id=workout_id, sportsman_id=sportsman_id
        )

    async def bind_sportsman_to_workouts(
        self, sportsman_id: UUID, workouts_ids: Sequence[UUID]
    ) -> None:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.PLANNED
        )
        assert workout_status_out is not None

        await self.repository.bind_sportsman_to_workouts(
            sportsman_id=sportsman_id,
            workouts_ids=workouts_ids,
            planned_status_id=workout_status_out.id,
        )

    async def unbind_sportsman_to_workouts(
        self, sportsman_id: UUID, workouts_ids: Sequence[UUID]
    ) -> None:
        await self.repository.unbind_sportsman_to_workouts(
            sportsman_id=sportsman_id,
            workouts_ids=workouts_ids,
        )

    async def planned(
        self, schema_in: schemas.CreateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.PLANNED
        )
        assert workout_status_out is not None

        return await self.repository.create(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

    async def in_progress(
        self, schema_in: schemas.UpdateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.IN_PROGRESS
        )
        assert workout_status_out is not None

        return await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

    async def completed(
        self, schema_in: schemas.UpdateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.COMPLETED
        )
        assert workout_status_out is not None

        updated_out = await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(schema_in.workout_id),  # type: ignore
            sportsman_id=str(schema_in.sportsman_id),  # type: ignore
        )
        await workouts_status_action.rmv_sportsman_skipped()

        return updated_out

    async def canceled(
        self, schema_in: schemas.UpdateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.CANCELED
        )
        assert workout_status_out is not None

        updated_out = await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(schema_in.workout_id),  # type: ignore
            sportsman_id=str(schema_in.sportsman_id),  # type: ignore
        )
        await workouts_status_action.rmv_sportsman_skipped()

        return updated_out

    async def skipped(
        self, schema_in: schemas.UpdateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.SKIPPED
        )
        assert workout_status_out is not None

        return await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

    async def active(
        self, schema_in: schemas.UpdateSportsmansWorkoutIn
    ) -> SportsmansWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.ACTIVE
        )
        assert workout_status_out is not None

        updated_out = await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )

        today = datetime.datetime.now()
        next_day = today + datetime.timedelta(days=1)
        formatted_day = next_day.replace(hour=0, minute=0, second=1, microsecond=0)
        exp_time = round((formatted_day - today).total_seconds())

        workouts_status_action = self.workouts_status_action_part(
            workout_id=str(schema_in.workout_id),  # type: ignore
            sportsman_id=str(schema_in.sportsman_id),  # type: ignore
        )
        await workouts_status_action.begin_sportsman_skipped(timeout=exp_time)

        return updated_out

    async def get_other_by_statuses(
        self,
        workout_id: UUID,
        self_sportsman_id: UUID,
        statuses: tuple[WorkoutsStatusesEnum, ...],
    ) -> Sequence[SportsmansWorkouts]:
        return await self.repository.get_other_by_statuses(
            workout_id=workout_id,
            self_sportsman_id=self_sportsman_id,
            statuses=statuses,
        )
