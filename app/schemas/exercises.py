from typing import Self
from uuid import UUID

from pydantic import Field, model_validator

from app.consts import BasicExercisesTypesEnum, SupportExercisesTypesEnum
from .exercises_types import ExercisesTypesOut

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateBasicExerciseIn(BaseSchema):
    type: BasicExercisesTypesEnum
    reps: int = Field(..., gt=0)
    sets: int = Field(..., gt=0)
    rest: float | None = Field(..., gt=0)

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
    rest: float | None = Field(..., gt=0)
    order: int


class CreateSupportExerciseIn(BaseSchema):
    type: SupportExercisesTypesEnum
    time: int = Field(..., gt=0)


class SupportExerciseOut(BaseSchemaFromDB):
    id: UUID
    type: ExercisesTypesOut
    time: int = Field(..., gt=0)
    order: int


class CreateExerciseInDB(BaseSchema):
    workout_pool_id: UUID
    type_id: UUID
    reps: int | None = None
    sets: int | None = None
    rest: float | None = None
    time: int | None = None
    order: int
