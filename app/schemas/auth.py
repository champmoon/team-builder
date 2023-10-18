from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema
from .validation import Password


class RefreshTokenIn(BaseSchema):
    refresh_token: UUID


class RegisterTrainerIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    name: str


class LoginTrainerIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class RegisterSportsmenIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    name: str


class LoginSportsmenIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class LoginrAdminIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
