from uuid import UUID

from .base_class import BaseSchema


class CreateSportsmansWorkoutIn(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID
    status_id: UUID
    execution_time: float | None = None
