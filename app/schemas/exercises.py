from typing import Self
from uuid import UUID

from pydantic import Field, model_validator

from app.schemas.utils import TimeFormat

from .base_class import BaseSchema, BaseSchemaFromDB
from .exercises_types import ExercisesTypesOut


class CreateBasicExerciseIn(BaseSchema):
    type: ExercisesTypesOut
    reps: int = Field(..., gt=0)
    sets: int = Field(..., gt=0)
    rest: TimeFormat | None

    @model_validator(mode="after")
    def check_sets_rest(self) -> Self:
        if self.sets == 1 and self.rest is not None:
            raise ValueError("because sets - 1, rest must be unset")
        return self


class BasicExerciseOut(BaseSchemaFromDB):
    id: UUID
    type: ExercisesTypesOut
    reps: int = Field(..., gt=0)
    sets: int = Field(..., gt=0)
    rest: TimeFormat | None
    # order: int


class CreateSupportExerciseIn(BaseSchema):
    type: ExercisesTypesOut
    time: TimeFormat


class SupportExerciseOut(BaseSchemaFromDB):
    id: UUID
    type: ExercisesTypesOut
    time: TimeFormat
    # order: int


class CreateExerciseInDB(BaseSchema):
    workout_pool_id: UUID
    type_id: UUID
    reps: int | None = None
    sets: int | None = None
    rest: TimeFormat | None = None
    time: TimeFormat | None = None
    order: int
