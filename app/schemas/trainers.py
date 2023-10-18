from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import Password


class CreateTrainerIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    name: str


class CreateTrainerInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    name: str


class UpdateTrainerIn(BaseSchema):
    name: str


class TrainerOut(BaseSchemaFromDB):
    id: UUID
    email: str
    name: str
