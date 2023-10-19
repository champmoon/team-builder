from uuid import UUID

from app.consts import UsersTypes

from .base_class import BaseSchema


class CreateSessionIn(BaseSchema):
    user_id: UUID
    refresh_token: UUID
    user_type: UsersTypes
