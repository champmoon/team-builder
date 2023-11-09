from typing import Any

from app.consts import WORKOUTS_STATUSES_DESC, WorkoutsStatusesEnum

from .base_class import BaseSchema


class WorkoutsStatusesOut(BaseSchema):
    status: WorkoutsStatusesEnum
    description: str

    @model_validator(mode="before")  # type: ignore
    def set_description(self) -> Any:
        self.description = WORKOUTS_STATUSES_DESC[WorkoutsStatusesEnum(self.type)]
        return self
