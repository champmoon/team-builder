from uuid import UUID

from pydantic import NaiveDatetime

from .base_class import BaseSchema, BaseSchemaFromDB
from .workouts_statuses import WorkoutsStatusesOut


class CreateTrainerWorkoutIn(BaseSchema):
    trainer_id: UUID
    workout_id: UUID
    status_id: UUID


class TrainerWorkoutOut(BaseSchemaFromDB):
    trainer_id: UUID
    workout_id: UUID
    name: str
    estimated_time: float
    status: WorkoutsStatusesOut
    date: NaiveDatetime
    created_at: NaiveDatetime
