from uuid import UUID

from .base_class import BaseSchema


class CreateSessionIn(BaseSchema):
    user_id: UUID
    refresh_token: UUID
