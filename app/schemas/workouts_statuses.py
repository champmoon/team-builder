from typing import Any

from app.consts import WORKOUTS_STATUSES_DESC, WorkoutsStatusesEnum
from pydantic import model_validator

from .base_class import BaseSchema


class WorkoutsStatusesOut(BaseSchema):
    status: WorkoutsStatusesEnum
    description: str

    @model_validator(mode="after")
    def set_description(self) -> Any:
        self.description = WORKOUTS_STATUSES_DESC[WorkoutsStatusesEnum(self.status)]
        return self

class CreateWorkoutStatusesIn(BaseSchema):
    status: WorkoutsStatusesEnum
