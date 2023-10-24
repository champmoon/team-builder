from app.consts import ExercisesTypesEnum

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateExercisesTypeIn(BaseSchema):
    type: ExercisesTypesEnum


class ExercisesTypesOut(BaseSchemaFromDB):
    type: int
    description: str
