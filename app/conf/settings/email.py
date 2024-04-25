from pydantic import EmailStr
from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: EmailStr
    EMAIL_HOST_PASSWORD: str
    DEFAULT_FROM_EMAIL: EmailStr
    EMAIL_USE_TLS: bool
    EMAIL_USE_SSL: bool
    CONFIRM_URL: str
