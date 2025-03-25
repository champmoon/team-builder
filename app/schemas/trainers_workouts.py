from uuid import UUID

from pydantic import NaiveDatetime

from app import consts

from .base_class import BaseSchema, BaseSchemaFromDB
from .exercises import BasicExerciseOut, SupportExerciseOut


class CreateTrainerWorkoutIn(BaseSchema):
    trainer_id: UUID
    workout_id: UUID


class UpdateTrainerWorkoutIn(BaseSchema):
    trainer_id: UUID
    workout_id: UUID


class TrainerWorkoutPoolOut(BaseSchemaFromDB):
    id: UUID
    name: str
    estimated_time: float
    created_at: NaiveDatetime
    exercises: list[BasicExerciseOut | SupportExerciseOut]


class TrainerWorkoutOut(BaseSchemaFromDB):
    id: UUID
    repeat_id: UUID
    name: str
    estimated_time: float
    rest_time: int
    price: int
    date: NaiveDatetime
    created_at: NaiveDatetime
    comment: str | None = None
    goal: str | None = None
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


class SportsmansWorkoutsManagmentIn(BaseSchema):
    workout_id: UUID
    sportsmans_ids: list[UUID] | None = None
