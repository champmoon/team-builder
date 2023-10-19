from uuid import UUID

from .base_class import BaseSchema, BaseSchemaFromDB
from .sportsmans import SportsmanForTeamOut


class CreateTeamIn(BaseSchema):
    trainer_id: UUID


class TeamOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    sportsmans: list[SportsmanForTeamOut]
