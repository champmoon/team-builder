from uuid import UUID

from pydantic import NaiveDatetime

from app import consts

from .base_class import BaseSchema, BaseSchemaFromDB
from .exercises import BasicExerciseOut, SupportExerciseOut
from .workouts_statuses import WorkoutsStatusesOut


class CreateSportsmansWorkoutIn(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID
    status_id: UUID
    execution_time: float | None = None


class SportsmansWorkoutOut(BaseSchemaFromDB):
    id: UUID
    name: str
    estimated_time: float
    rest_time: int
    stress_questionnaire_time: int
    date: NaiveDatetime
    created_at: NaiveDatetime
    status: WorkoutsStatusesOut
    exercises: list[BasicExerciseOut | SupportExerciseOut]


class SportsmansSportsmanWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.INDIVIDUAL
    sportsman_id: UUID


class SportsmansGroupWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.GROUP
    group_id: UUID


class SportsmansTeamWorkoutOut(SportsmansWorkoutOut):
    workout_type: consts.WorkoutsTypes = consts.WorkoutsTypes.TEAM
    team_id: UUID
