from pydantic import EmailStr, Field

from .base_class import BaseSchema
from .validation import Password


class CreateAdminIn(BaseSchema):
    email: EmailStr
    password: Password = Field(min_length=5, max_length=30)


class CreateAdminInDB(BaseSchema):
    email: EmailStr
    hashed_password: str
