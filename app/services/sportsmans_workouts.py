from typing import Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
from app.consts import WorkoutsStatusesEnum
from app.models import SportsmansWorkouts
from app.repositories import SportsmansWorkoutsRepository, WorkoutsStatusesRepository


class SportsmansWorkoutsService:
    def __init__(
        self,
        repository: SportsmansWorkoutsRepository,
        statuses_repository: WorkoutsStatusesRepository,
    ) -> None:
        self.repository = repository
        self.statuses_repository = statuses_repository

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

        return await self.repository.update_status(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )
