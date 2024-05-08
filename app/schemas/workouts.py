from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import EmailStr, Field, NaiveDatetime, model_validator

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
    rest_time: int = Field(..., ge=0)
    stress_questionnaire_time: int = Field(..., ge=1)
    comment: str | None = None
    goal: str | None = None


class CreateWorkoutForSportsmanIn(BaseSchema):
    workout_pool_id: UUID
    sportsman_email: EmailStr
    date: NaiveDatetime
    rest_time: int = Field(..., ge=0)
    stress_questionnaire_time: int = Field(..., ge=1)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class CreateWorkoutForGroupIn(BaseSchema):
    workout_pool_id: UUID
    group_id: UUID
    date: NaiveDatetime
    rest_time: int = Field(..., ge=0)
    stress_questionnaire_time: int = Field(..., ge=1)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class CreateWorkoutForTeamIn(BaseSchema):
    workout_pool_id: UUID
    date: NaiveDatetime
    rest_time: int = Field(..., ge=0)
    stress_questionnaire_time: int = Field(..., ge=1)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")
        return self


class UpdateWorkoutPoolIn(BaseSchema):
    name: str | None = None
    estimated_time: float | None = None
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn] | None = None

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        if self.name is None and self.estimated_time is None and self.exercises is None:
            raise ValueError("at least not null")
        return self


class UpdateWorkoutIn(BaseSchema):
    date: NaiveDatetime | None = None
    rest_time: int | None = Field(None, ge=0)
    stress_questionnaire_time: int | None = Field(None, ge=1)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        if self.date and self.date <= (now := datetime.utcnow()):
            raise ValueError(f"date - {self.date} less then now - {now}")

        if not any((
            self.date is None,
            self.rest_time is None,
            self.stress_questionnaire_time is None,
            self.comment is None,
            self.goal is None,
        )):
            raise ValueError("at least not null")

        return self
