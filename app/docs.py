from typing import Literal

from app.conf.settings import settings

AppDocs = dict[Literal["title", "description", "summary"], str]

app_docs: AppDocs = {
    "title": "Team-Builder",
    "description": (
        "* **[Авторизация](https://tbuilder.pro/docs#/%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)**\n\n"
        "* **[Типы упражнения](https://tbuilder.pro/docs#/%D0%A2%D0%B8%D0%BF%D1%8B%20%D1%83%D0%BF%D1%80%D0%B0%D0%B6%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F)**\n\n"
        "* **[Статусы тренировок](https://tbuilder.pro/docs#/C%D1%82%D0%B0%D1%82%D1%83%D1%81%D1%8B%20%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D0%BA)**\n\n"
        "* **[Тренеры](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)**\n\n"
        "> * **[Регистрация](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)**\n\n"
        "> * **[Профиль](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%9F%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8C)**\n\n"
        "> * **[Анкета](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%90%D0%BD%D0%BA%D0%B5%D1%82%D0%B0)**\n\n"
        "> * **[Команда](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0)**\n\n"
        "> * **[Группа](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%93%D1%80%D1%83%D0%BF%D0%BF%D0%B0)**\n\n"
        "> * **[Типы упражнения](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A2%D0%B8%D0%BF%D1%8B%20%D1%83%D0%BF%D1%80%D0%B0%D0%B6%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F)**\n\n"
        "> * **[Тренировка](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A2%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0)**\n\n"
        "> * **[Управление тренировкой](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%BE%D0%B9)**\n\n"
        "> * **[Программа тренировок](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%20%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D0%BA)**\n\n"
        "> * **[Опросник по нагрузке](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%9E%D0%BF%D1%80%D0%BE%D1%81%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B5)**\n\n"
        "> * **[Опросник по здоровью](https://tbuilder.pro/docs#/%D0%A2%D1%80%D0%B5%D0%BD%D0%B5%D1%80%D1%8B%20%E2%86%92%20%D0%9E%D0%BF%D1%80%D0%BE%D1%81%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20%D0%B7%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D1%8C%D1%8E)**\n\n"
        "* **[Спортсмены](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)**\n\n"
        "> * **[Регистрация](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F)**\n\n"
        "> * **[Профиль](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%9F%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8C)**\n\n"
        "> * **[Анкета](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%90%D0%BD%D0%BA%D0%B5%D1%82%D0%B0)**\n\n"
        "> * **[Команда](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B0)**\n\n"
        "> * **[Группа](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%93%D1%80%D1%83%D0%BF%D0%BF%D0%B0)**\n\n"
        "> * **[Тренировка](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%A2%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0)**\n\n"
        "> * **[Управление тренировкой](https://tbuilder.pro/docs#/%D0%A1%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%A3%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%BE%D0%B9)**\n\n"
        "> * **[Опросник по нагрузке](https://tbuilder.pro/docs#/C%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%9E%D0%BF%D1%80%D0%BE%D1%81%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B5)**\n\n"
        "> * **[Опросник по здоровью](https://tbuilder.pro/docs#/C%D0%BF%D0%BE%D1%80%D1%82%D1%81%D0%BC%D0%B5%D0%BD%D1%8B%20%E2%86%92%20%D0%9E%D0%BF%D1%80%D0%BE%D1%81%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20%D0%B7%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%D1%8C%D1%8E)**\n\n"
        + f"""\n
    DEBUG MODE - {settings.DEBUG}
    """
    ),
}
