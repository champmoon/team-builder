from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema
from .validation import Password


class RefreshTokenIn(BaseSchema):
    refresh_token: UUID


class RegisterIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    name: str
    is_trainer: bool


class LoginIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
