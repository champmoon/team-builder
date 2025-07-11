from uuid import UUID

from pydantic import EmailStr, Field

from .base_class import BaseSchema, BaseSchemaFromDB
from .validation import BaseAtLeastOneFieldValidator, Password
from .workouts_statuses import WorkoutsStatusesOut


class CreateSportsmanIn(BaseSchema):
    team_id: UUID | None = None
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class CreateLocalSportsmanIn(BaseSchema):
    first_name: str
    middle_name: str | None = None
    last_name: str | None = None


class CreateSportsmanInDB(BaseSchema):
    team_id: UUID | None = None
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class CreateLocalSportsmanInDB(BaseSchema):
    team_id: UUID
    first_name: str
    middle_name: str | None = None
    last_name: str | None = None


class UpdateSportsmanIn(BaseSchema, BaseAtLeastOneFieldValidator):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


class MergeLocalSportsman(BaseSchema):
    local_sportsman_id: UUID
    email: EmailStr


class SportsmanOut(BaseSchemaFromDB):
    id: UUID
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    avatar_uri: str | None = None


class SportsmanForTeamOut(BaseSchemaFromDB):
    id: UUID
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    avatar_uri: str | None = None


class SportsmanForGroupOut(BaseSchemaFromDB):
    id: UUID
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    avatar_uri: str | None = None


class ListSportsmansEmailsIn(BaseSchema):
    sportsmans_emails: list[EmailStr]


class SportsmansEmailIn(BaseSchema):
    sportsman_email: EmailStr


class InviteSportsmanToTeamIn(BaseSchema):
    email: EmailStr
    local_sportsman_id: UUID | None = None


class OnlyGroupOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str


class SportsmanWithGroupsOut(BaseSchemaFromDB):
    id: UUID
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    team_id: UUID | None = None
    avatar_uri: str | None = None
    groups: list[OnlyGroupOut]


class SportsmanWithWorkoutStatusOut(BaseSchema):
    sportsman_id: UUID
    workout_id: UUID
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    status: WorkoutsStatusesOut


class UpdateSportsmanPasswordIn(BaseSchema):
    password: str


class InnerUpdateSportsmanPasswordIn(BaseSchema):
    hashed_password: str
