from pydantic_settings import BaseSettings


class AdminSettings(BaseSettings):
    FIRST_ADMIN_EMAIL: str
    FIRST_ADMIN_PASSWORD: str
