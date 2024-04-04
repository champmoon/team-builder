from typing import Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
from app.consts import WorkoutsStatusesEnum
from app.models import TrainersWorkouts
from app.repositories import TrainersWorkoutsRepository, WorkoutsStatusesRepository


class TrainersWorkoutsService:
    def __init__(
        self,
        repository: TrainersWorkoutsRepository,
        statuses_repository: WorkoutsStatusesRepository,
    ) -> None:
        self.repository = repository
        self.statuses_repository = statuses_repository

    async def get_all_by_trainer_id(
        self,
        trainer_id: UUID,
        offset: int = 0,
        limit: int = 100,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[TrainersWorkouts]:
        return await self.repository.get_all_by_trainer_id(
            trainer_id=trainer_id,
            offset=offset,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[TrainersWorkouts]:
        return await self.repository.get_all_by_workout_id(workout_id=workout_id)

    async def get_by(
        self, workout_id: UUID, trainer_id: UUID
    ) -> TrainersWorkouts | None:
        return await self.repository.get_by(
            workout_id=workout_id, trainer_id=trainer_id
        )

    async def planned(
        self, schema_in: schemas.CreateTrainerWorkoutIn
    ) -> TrainersWorkouts:
        workout_status_out = await self.statuses_repository.get_by_status(
            status=WorkoutsStatusesEnum.PLANNED
        )
        assert workout_status_out is not None

        return await self.repository.create(
            schema_in=schema_in,
            status_id=workout_status_out.id,
        )
