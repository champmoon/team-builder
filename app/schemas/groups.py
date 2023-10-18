from uuid import UUID

from pydantic import EmailStr

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateGroupIn(BaseSchema):
    email: EmailStr
    trainer_id: UUID


class UpdateGroupIn(BaseSchema):
    name: str


class GroupOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str
