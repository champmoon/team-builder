from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import BaseAtLeastOneFieldValidator, Password


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


class UpdateTrainerIn(BaseSchema, BaseAtLeastOneFieldValidator):
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


class UpdateTrainerPasswordIn(BaseSchema):
    password: str


class InnerUpdateTrainerPasswordIn(BaseSchema):
    hashed_password: str
