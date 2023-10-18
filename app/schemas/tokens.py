from uuid import UUID

from app.consts import UsersTypes

from .base_class import BaseSchema


class RefreshIn(BaseSchema):
    refresh_token: UUID


class TokensEncodedSchema(BaseSchema):
    user_id: str
    user_type: UsersTypes


class TokensDecodedSchema(BaseSchema):
    user_id: str
    user_type: UsersTypes


class TokensOut(BaseSchema):
    access_token: str
    refresh_token: UUID
    user_type: UsersTypes
