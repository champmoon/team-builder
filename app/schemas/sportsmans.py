from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import Password


class CreateSportsmanIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    name: str


class CreateSportsmanInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
    name: str


class UpdateSportsmanIn(BaseSchema):
    name: str


class SportsmanOut(BaseSchemaFromDB):
    id: UUID
    email: str
    name: str
    team_id: UUID | None = None
