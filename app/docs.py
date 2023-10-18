from typing import Literal

from app.conf.settings import settings

app_docs: dict[Literal["title", "description", "summary"], str] = {
    "title": "Team-Builder",
    "description": f"""

    DEBUG MODE - {settings.DEBUG}
    """,
}
