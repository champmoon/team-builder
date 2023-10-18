from uuid import UUID

from pydantic import EmailStr

from .base_class import BaseSchema, BaseSchemaFromDB


class CreateTeamIn(BaseSchema):
    email: EmailStr
    trainer_id: UUID


class TeamOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
