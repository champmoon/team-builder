from typing import Any

from pydantic import model_validator

from app import consts
from app.consts import EXERCISES_TYPES_DESC, ExercisesTypesEnum

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateExercisesTypeIn(BaseSchema):
    type: ExercisesTypesEnum


class ExercisesTypesOut(BaseSchemaFromDB):
    type: int
    description: str | None = None
    is_basic: bool = True

    @model_validator(mode="after")
    def set_description(self) -> Any:
        self.description = EXERCISES_TYPES_DESC[ExercisesTypesEnum(self.type)]
        return self

    @model_validator(mode="after")
    def set_is_basic(self) -> Any:
        try:
            consts.BasicExercisesTypesEnum(self.type)
        except ValueError:
            self.is_basic = False

        return self
