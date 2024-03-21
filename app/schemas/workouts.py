from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import EmailStr, NaiveDatetime, model_validator

from .base_class import BaseSchema
from .exercises import CreateBasicExerciseIn, CreateSupportExerciseIn


class CreateWorkoutPoolInDB(BaseSchema):
    name: str
    trainer_id: UUID
    estimated_time: float


class CreateWorkoutPoolIn(BaseSchema):
    name: str
    estimated_time: float
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn]


class CreateWorkoutInDB(BaseSchema):
    workout_pool_id: UUID
    date: NaiveDatetime


class CreateWorkoutForSportsmanIn(BaseSchema):
    workout_pool_id: UUID
    sportsman_email: EmailStr
    date: NaiveDatetime

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class CreateWorkoutForGroupIn(BaseSchema):
    workout_pool_id: UUID
    group_id: UUID
    date: NaiveDatetime

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class CreateWorkoutForTeamIn(BaseSchema):
    workout_pool_id: UUID
    date: NaiveDatetime

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class UpdateWorkoutPoolIn(BaseSchema):
    name: str | None = None
    estimated_time: float | None = None

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        if not any((self.name, self.estimated_time)):
            raise ValueError("at least not null")
        return self


class UpdateWorkoutIn(BaseSchema):
    date: NaiveDatetime

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self

