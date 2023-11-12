from datetime import datetime
from uuid import UUID

from pydantic import NaiveDatetime, model_validator

from .base_class import BaseSchema
from .exercises import CreateBasicExerciseIn, CreateSupportExerciseIn


class CreateWorkoutInDB(BaseSchema):
    name: str
    estimated_time: int
    date: NaiveDatetime

    # TODO
    @model_validator(mode="after")
    def check_date(self):
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")


class BaseCreateWorkoutIn(BaseSchema):
    name: str
    date: NaiveDatetime
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn]


class CreateWorkoutForSportsmanIn(BaseCreateWorkoutIn):
    sportsman_id: UUID


class CreateWorkoutForGroupIn(BaseCreateWorkoutIn):
    group_id: UUID


class CreateWorkoutForTeamIn(BaseCreateWorkoutIn): ...
