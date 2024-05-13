from .base_class import BaseSchema, BaseSchemaFromDB


class CreateExercisesTypeIn(BaseSchema):
    type: int
    description: str
    is_basic: bool


class UpdateExercisesTypeIn(BaseSchema):
    type: int
    description: str
    is_basic: bool


class ExercisesTypesOut(BaseSchemaFromDB):
    type: int
    description: str
    is_basic: bool
