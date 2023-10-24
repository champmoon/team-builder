from typing import Any

from pydantic import model_validator

from app.consts import EXERCISES_TYPES_DESC, ExercisesTypesEnum

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateExercisesTypeIn(BaseSchema):
    type: ExercisesTypesEnum


class ExercisesTypesOut(BaseSchemaFromDB):
    type: int
    description: str

    @model_validator(mode="before")  # type: ignore
    def set_description(self) -> Any:
        self.description = EXERCISES_TYPES_DESC[ExercisesTypesEnum(self.type)]
        return self
