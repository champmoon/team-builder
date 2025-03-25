from uuid import UUID

from pydantic import NaiveDatetime

from app import consts

from .base_class import BaseSchema, BaseSchemaFromDB
from .exercises import BasicExerciseOut, SupportExerciseOut


class CreateSportsmansWorkoutIn(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID
    execution_time: float | None = None


class UpdateSportsmansWorkoutIn(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID


class SportsmansWorkoutOut(BaseSchemaFromDB):
    id: UUID
    repeat_id: UUID
    name: str
    estimated_time: float
    rest_time: int
    price: int
    date: NaiveDatetime
    created_at: NaiveDatetime
    # status: WorkoutsStatusesOut
    is_paid: bool
    is_attend: bool
    comment: str | None = None
    goal: str | None = None
    exercises: list[BasicExerciseOut | SupportExerciseOut]
    sportsman_id: UUID


class SportsmansSportsmanWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.INDIVIDUAL


class SportsmansGroupWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.GROUP
    group_id: UUID


class SportsmansTeamWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.TEAM
    team_id: UUID
