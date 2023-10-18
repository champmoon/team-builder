from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ToolsSettings(BaseSettings):
    FORMAT_DIRS: tuple[str, ...] = (
        "app",
        "migrations",
    )
    LINT_DIRS: tuple[str, ...] = ("app",)


config = ToolsSettings()
