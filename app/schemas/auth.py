from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema
from .validation import Password


class ConfirmTokenIn(BaseSchema):
    confirm_token: UUID


class RefreshTokenIn(BaseSchema):
    refresh_token: UUID


class TrainerRegisterIn(BaseSchema):
    email: EmailStr
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    # team_name: str
    # sport_type: SportsTypes
    password: Password = Field(min_length=5, max_length=30)


class SportsmanRegisterIn(BaseSchema):
    trainer_id: UUID
    email: EmailStr
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    password: Password = Field(min_length=5, max_length=30)


class LoginIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class SendTrainerEmailIn(BaseSchema):
    email: EmailStr
    # first_name: str | None = None
    # middle_name: str | None = None
    # last_name: str | None = None
    # team_name: str
    # sport_type: SportsTypes


class TrainerEmailConfirmOut(BaseSchema):
    email: EmailStr
    # first_name: str | None = None
    # middle_name: str | None = None
    # last_name: str | None = None
    # team_name: str
    # sport_type: SportsTypes


class SendSportsmanEmailIn(BaseSchema):
    email: EmailStr


class InnerSendSportsmanEmailIn(BaseSchema):
    email: EmailStr
    # sport_type: SportsTypes
    trainer_id: UUID


class SportsmanEmailConfirmOut(BaseSchema):
    email: EmailStr
    # sport_type: SportsTypes
    trainer_id: UUID
