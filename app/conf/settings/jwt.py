from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
