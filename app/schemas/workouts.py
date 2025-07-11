import datetime
from typing import Self
from uuid import UUID

from pydantic import Field, NaiveDatetime, model_validator

from app.schemas.utils import TimeFormat

from .base_class import BaseSchema
from .exercises import CreateBasicExerciseIn, CreateSupportExerciseIn


class CreateWorkoutPoolInDB(BaseSchema):
    name: str
    trainer_id: UUID
    estimated_time: TimeFormat
    created_at: NaiveDatetime | None = None


class CreateWorkoutPoolIn(BaseSchema):
    name: str
    estimated_time: TimeFormat
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn]


class CreateWorkoutInDB(BaseSchema):
    workout_pool_id: UUID
    date: NaiveDatetime
    rest_time: TimeFormat
    price: int = Field(..., ge=0)
    comment: str | None = None
    goal: str | None = None
    repeat_id: UUID | None = None


class CreateWorkoutForSportsmanIn(BaseSchema):
    workout_pool_id: UUID
    sportsman_id: UUID
    dates: list[NaiveDatetime]
    rest_time: TimeFormat
    price: int = Field(..., ge=0)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class RepeatWorkoutForSportsmanIn(BaseSchema):
    workout_id: UUID
    sportsman_id: UUID
    dates: list[NaiveDatetime]

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class CreateWorkoutForGroupIn(BaseSchema):
    workout_pool_id: UUID
    group_id: UUID
    dates: list[NaiveDatetime]
    rest_time: TimeFormat
    price: int = Field(..., ge=0)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class RepeatWorkoutForGroupIn(BaseSchema):
    workout_id: UUID
    group_id: UUID
    dates: list[NaiveDatetime]

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class CreateWorkoutForTeamIn(BaseSchema):
    workout_pool_id: UUID
    dates: list[NaiveDatetime]
    rest_time: TimeFormat
    price: int = Field(..., ge=0)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class RepeatWorkoutForTeamIn(BaseSchema):
    workout_id: UUID
    dates: list[NaiveDatetime]

    @model_validator(mode="after")
    def check_date(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        for date in self.dates:
            if date <= now:
                raise ValueError(f"date - {date} less then now - {now}")
        return self


class UpdateWorkoutPoolIn(BaseSchema):
    name: str | None = None
    estimated_time: TimeFormat | None = None
    exercises: list[CreateBasicExerciseIn | CreateSupportExerciseIn] | None = None

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        if self.name is None and self.estimated_time is None and self.exercises is None:
            raise ValueError("at least not null")
        return self


class UpdateWorkoutIn(BaseSchema):
    date: NaiveDatetime | None = None
    rest_time: TimeFormat | None
    price: int | None = Field(None, ge=0)
    comment: str | None = None
    goal: str | None = None

    @model_validator(mode="after")
    def check_at_least(self) -> Self:
        now = datetime.timedelta(hours=3) + datetime.datetime.now(datetime.UTC).replace(
            tzinfo=None
        )
        if self.date and self.date <= now:
            raise ValueError(f"date - {self.date} less then now - {now}")

        if (
            self.date is None
            and self.rest_time is None
            and self.price is None
            and self.comment is None
            and self.goal is None
        ):
            raise ValueError("at least not null")

        return self
