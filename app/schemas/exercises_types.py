from typing import Any

from pydantic import model_validator

from app.consts import EXERCISES_TYPES_DESC, ExercisesTypesEnum

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateExercisesTypeIn(BaseSchema):
    type: ExercisesTypesEnum
    average_time: float | None


class ExercisesTypesOut(BaseSchemaFromDB):
    type: int
    average_time: float | None
    description: str | None = None

    @model_validator(mode="after")
    def set_description(self) -> Any:
        self.description = EXERCISES_TYPES_DESC[ExercisesTypesEnum(self.type)]
        return self
