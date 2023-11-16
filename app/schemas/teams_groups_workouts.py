from uuid import UUID


from .base_class import BaseSchema


class CreateTeamGroupWorkoutIn(BaseSchema):
    team_id: UUID | None = None
    group_id: UUID | None = None
    workout_id: UUID
