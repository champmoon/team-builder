from typing import Literal

from app.conf.settings import settings

AppDocs = dict[Literal["title", "description", "summary"], str]

app_docs: AppDocs = {
    "title": "Team-Builder",
    "description": (
        "***[Trainers"
        " API](http://158.160.118.208/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)***"
        + "\n\n ***[Sportsmans"
        " API](http://158.160.118.208/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)***"
        + f"""\n
    DEBUG MODE - {settings.DEBUG}
    """
    ),
}
