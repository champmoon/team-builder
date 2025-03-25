from uuid import UUID

from pydantic import EmailStr, Field

from app.consts import UsersTypes

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import Password


class ConfirmTokenIn(BaseSchema):
    confirm_token: UUID


class AccessTokenIn(BaseSchema):
    access_token: str


class RefreshTokenIn(BaseSchema):
    refresh_token: UUID


class VerifyResponse(BaseSchema):
    user_type: UsersTypes


# class TrainerRegisterIn(BaseSchema):
#     email: EmailStr
#     first_name: str | None = None
#     middle_name: str | None = None
#     last_name: str | None = None
#     # team_name: str
#     # sport_type: SportsTypes
#     password: Password = Field(min_length=5, max_length=30)


# class SportsmanRegisterIn(BaseSchema):
#     trainer_id: UUID
#     email: EmailStr
#     first_name: str | None = None
#     middle_name: str | None = None
#     last_name: str | None = None
#     password: Password = Field(min_length=5, max_length=30)


class RegisterIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class ResetPasswordIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class LoginIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    remember_me: bool = False
    # first_name: str | None = None
    # middle_name: str | None = None
    # last_name: str | None = None
    # team_name: str
    # sport_type: SportsTypes
    # first_name: str | None = None
    # middle_name: str | None = None
    # last_name: str | None = None
    # team_name: str
    # sport_type: SportsTypes


# class SendTrainerEmailIn(BaseSchema):
#     email: EmailStr


# class TrainerEmailConfirmOut(BaseSchema):
#     email: EmailStr


class SendEmailIn(BaseSchema):
    email: EmailStr
    user_type: UsersTypes


class EmailConfirmOut(BaseSchema):
    email: EmailStr


class PasswordConfirmOut(BaseSchema):
    email: EmailStr


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


class ClientOut(BaseSchemaFromDB):
    id: UUID
    email: str


class SendPasswordIn(BaseSchema):
    email: EmailStr
