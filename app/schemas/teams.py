from uuid import UUID

from .base_class import BaseSchema, BaseSchemaFromDB
from .sportsmans import SportsmanForTeamOut


class CreateTeamIn(BaseSchema):
    trainer_id: UUID
    # name: str
    # sport_type: str


class TeamOut(BaseSchemaFromDB):
    id: UUID
    trainer_id: UUID
    # name: str
    # sport_type: str
    sportsmans: list[SportsmanForTeamOut]


class TeamInviteLink(BaseSchema):
    link: str
