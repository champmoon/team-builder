from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import Password


class CreateTrainerIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class CreateTrainerInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class UpdateTrainerIn(BaseSchema):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class TrainerOut(BaseSchemaFromDB):
    id: UUID
    email: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    avatar_uri: str | None = None
