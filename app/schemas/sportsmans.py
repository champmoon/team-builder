from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import Password


class CreateSportsmanIn(BaseSchema):
    team_id: UUID
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class CreateSportsmanInDB(BaseSchema):
    team_id: UUID
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class UpdateSportsmanIn(BaseSchema):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class SportsmanOut(BaseSchemaFromDB):
    id: UUID
    email: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    avatar_uri: str | None = None


class SportsmanForTeamOut(BaseSchemaFromDB):
    id: UUID
    email: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    avatar_uri: str | None = None


class SportsmanForGroupOut(BaseSchemaFromDB):
    id: UUID
    email: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    avatar_uri: str | None = None


class ListSportsmansEmailsIn(BaseSchema):
    sportsmans_emails: list[EmailStr]


class SportsmansEmailIn(BaseSchema):
    sportsman_email: EmailStr


class OnlyGroupOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str


class SportsmanWithGroupsOut(BaseSchemaFromDB):
    id: UUID
    email: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    avatar_uri: str | None = None
    groups: list[OnlyGroupOut]
