from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("ASYNC_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: PostgresDsn | None, values: dict[str, str]
    ) -> PostgresDsn:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_HOST"],
            port=int(values["POSTGRES_PORT"]),
            path=values["POSTGRES_DB"],
        )
