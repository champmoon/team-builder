from uuid import UUID

from .base_class import BaseSchema


class CreateSportsmanGroupIn(BaseSchema):
    sportsman_id: UUID
    group_id: UUID


class DeleteSportsmanGroupIn(BaseSchema):
    sportsman_id: UUID
    group_id: UUID
