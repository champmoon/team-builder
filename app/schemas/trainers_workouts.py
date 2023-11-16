from uuid import UUID

from pydantic import NaiveDatetime

from app import consts

from .base_class import BaseSchema, BaseSchemaFromDB
from .workouts_statuses import WorkoutsStatusesOut
from .exercises import ExerciseOut


class CreateTrainerWorkoutIn(BaseSchema):
    trainer_id: UUID
    workout_id: UUID
    status_id: UUID


class TrainerWorkoutOut(BaseSchemaFromDB):
    workout_id: UUID
    name: str
    estimated_time: float
    status: WorkoutsStatusesOut
    date: NaiveDatetime
    created_at: NaiveDatetime
    exercises: list[ExerciseOut]


class TrainerSportsmanWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes
    sportsman_id: UUID


class TrainerGroupWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes
    group_id: UUID


class TrainerTeamWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes
    team_id: UUID
