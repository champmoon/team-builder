from uuid import UUID

from .base_class import BaseSchema, BaseSchemaFromDB
from .sportsmans import SportsmanForTeamOut


class CreateTeamIn(BaseSchema):
    trainer_id: UUID
    name: str


class TeamOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    name: str
    sportsmans: list[SportsmanForTeamOut]
