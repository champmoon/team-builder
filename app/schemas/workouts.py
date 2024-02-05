from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import EmailStr, NaiveDatetime, model_validator

from .base_class import BaseSchema
from .exercises import CreateBasicExerciseIn, CreateSupportExerciseIn


class CreateWorkoutInDB(BaseSchema):
    name: str
    estimated_time: float
    date: NaiveDatetime


class CreateWorkoutIn(BaseSchema):
    name: str
    date: NaiveDatetime
    estimated_time: float
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn]

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class CreateWorkoutForSportsmanIn(CreateWorkoutIn):
    sportsman_email: EmailStr


class CreateWorkoutForGroupIn(CreateWorkoutIn):
    group_id: UUID


class CreateWorkoutForTeamIn(CreateWorkoutIn): ...


class UpdateWorkoutIn(BaseSchema):
    name: str | None = None
    estimated_time: float | None = None
    date: NaiveDatetime | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date and self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        if not any((self.name, self.date)):
            raise ValueError("at least not null")
        return self
