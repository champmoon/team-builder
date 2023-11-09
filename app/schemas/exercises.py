from uuid import UUID

from pydantic import Field, model_validator

from app.consts import BasicExercisesTypesEnum

from .base_class import BaseSchema
from .exercises_types import ExercisesTypesOut


class CreateBasicExerciseIn(BaseSchema):
    type: BasicExercisesTypesEnum
    reps: int = Field(..., gt=0)
    sets: int = Field(..., gt=0)
    rest: int | None = Field(..., gt=0)
    order: int = Field(..., gt=0)

    # TODO
    @model_validator("after")
    def check_sets_rest(self):
        if self.sets == 1 and self.rest is not None:
            raise ValueError("because sets - 1, rest must be unset")


class CreateSupportExerciseIn(BaseSchema):
    type: ExercisesTypesOut
    time: int = Field(..., gt=0)


class ExerciseOut(BaseSchema):
    type: ExercisesTypesOut
    reps: int | None = None
    sets: int | None = None
    rest: int | None = None
    time: int | None = None
    order: int


class CreateExerciseInDB(BaseSchema):
    workout_id: UUID
    type_id: UUID
    reps: int | None = None
    sets: int | None = None
    rest: int | None = None
    time: int | None = None
    order: int
