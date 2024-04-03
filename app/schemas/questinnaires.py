from uuid import UUID

from pydantic import Field, NaiveDatetime

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateStressQuestionnaireIn(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID
    rating: int = 0


class UpdateStressQuestionnaireIn(BaseSchema):
    rating: int = Field(..., gt=0, lt=11)
    text: str | None = None


class StressQuestionnaireOut(BaseSchemaFromDB):
    id: UUID
    sportsman_id: UUID
    workout_id: UUID
    rating: int
    text: str | None
    created_at: NaiveDatetime


class CreateHealthQuestionnaireIn(BaseSchema):
    sportsman_id: UUID
    rating: int = 0


class UpdateHealthQuestionnaireIn(BaseSchema):
    rating: int = Field(..., gt=0, lt=11)
    text: str | None = None


class HealthQuestionnaireOut(BaseSchemaFromDB):
    id: UUID
    sportsman_id: UUID
    rating: int
    text: str | None
    created_at: NaiveDatetime
