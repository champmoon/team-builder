from uuid import UUID

from pydantic import EmailStr

from .base_class import BaseSchema, BaseSchemaFromDB
from .sportsmans import SportsmanForGroupOut


class CreateGroupIn(BaseSchema):
    name: str
    sportsmans_emails: list[EmailStr] | None = None


class AddSportsmansToGroupIn(BaseSchema):
    group_id: UUID
    sportsmans_emails: list[EmailStr] | None = None


class AddSportsmanToGroupIn(BaseSchema):
    group_id: UUID
    sportsman_email: EmailStr


class CreateGroupInDB(BaseSchema):
    trainer_id: UUID
    name: str


class UpdateGroupIn(BaseSchema):
    name: str


class GroupOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str
    sportsmans: list[SportsmanForGroupOut]
