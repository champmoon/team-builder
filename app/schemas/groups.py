from uuid import UUID

from .base_class import BaseSchema, BaseSchemaFromDB
from .sportsmans import SportsmanForGroupOut


class CreateGroupIn(BaseSchema):
    name: str
    # sportsmans_emails: list[EmailStr] | None = None
    sportsmans_ids: list[UUID] | None = None


class SportsmansToGroupIn(BaseSchema):
    group_id: UUID
    sportsmans_ids: list[UUID] | None = None


class SportsmanToGroupIn(BaseSchema):
    group_id: UUID
    sportsman_id: UUID


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


class OnlyGroupOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str


class ListGroupsIDsIn(BaseSchema):
    groups_ids: list[UUID]
