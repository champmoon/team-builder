from uuid import UUID

from pydantic import NaiveDatetime

from app import consts

from .base_class import BaseSchema, BaseSchemaFromDB
from .exercises import BasicExerciseOut, SupportExerciseOut
from .workouts_statuses import WorkoutsStatusesOut


class CreateTrainerWorkoutIn(BaseSchema):
    trainer_id: UUID
    workout_id: UUID
    status_id: UUID


class TrainerWorkoutPoolOut(BaseSchemaFromDB):
    id: UUID
    name: str
    estimated_time: float
    created_at: NaiveDatetime
    exercises: list[BasicExerciseOut | SupportExerciseOut]


class TrainerWorkoutOut(BaseSchemaFromDB):
    workout_id: UUID
    name: str
    estimated_time: float
    status: WorkoutsStatusesOut
    date: NaiveDatetime
    created_at: NaiveDatetime
    exercises: list[BasicExerciseOut | SupportExerciseOut]


class TrainerSportsmanWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.INDIVIDUAL
    sportsman_id: UUID


class TrainerGroupWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.GROUP
    group_id: UUID


class TrainerTeamWorkoutOut(TrainerWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.TEAM
    team_id: UUID
