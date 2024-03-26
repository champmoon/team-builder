from app.consts.sports_types import SportsTypes

DEFAULT_MAIN_DATA = [
    {
        "key": "gender",
        "label": "Пол",
        "type": "select",
        "options": ["Мужской", "Женский", "Боинг Б-52 «Стратофортресс»"],
        "required": True,
    },
    {
        "key": "position",
        "label": "Игровая позиция",
        "type": "text",
        "required": True,
    },
    {
        "key": "height",
        "label": "Рост",
        "type": "number",
        "required": True,
    },
    {
        "key": "weight",
        "label": "Вес",
        "type": "number",
        "required": True,
    },
    {
        "key": "age",
        "label": "Возраст",
        "type": "number",
        "required": True,
    },
]

DEFAULT_ADD_DATA = [
    {
        "key": "heartrate",
        "label": "Средняя частота сердцебиения",
        "type": "number",
        "required": True,
    },
    {
        "label": "Физическая подготовка",
        "type": "groups",
        "groups": [
            {
                "label": "Жим лежа",
                "fields": [
                    {
                        "key": "result1",
                        "label": "Результат актуальный",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "key": "force1",
                        "label": "Относил. Сила",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "label": "Норма World Class",
                        "type": "info1",
                        "value": "> 1.4",
                    },
                ],
            },
            {
                "label": "Приседания (кг)",
                "fields": [
                    {
                        "key": "result2",
                        "label": "Результат актуальный",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "key": "force2",
                        "label": "Относил. Сила",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "label": "Норма World Class",
                        "type": "info2",
                        "value": "> 1.7",
                    },
                ],
            },
            {
                "label": "10м (с)",
                "fields": [
                    {
                        "key": "result3",
                        "label": "Результат актуальный",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "key": "force3",
                        "label": "Относил. Сила",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "label": "Норма World Class",
                        "type": "info3",
                        "value": "Нап. < 1.7, Защ. < 1.6",
                    },
                ],
            },
            {
                "label": "30м (с)",
                "fields": [
                    {
                        "key": "result4",
                        "label": "Результат актуальный",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "key": "force4",
                        "label": "Относил. Сила",
                        "type": "number",
                        "required": True,
                    },
                    {
                        "label": "Норма World Class",
                        "type": "info4",
                        "value": "Нап. < 4.2, Защ. < 4.0",
                    },
                ],
            },
            {
                "label": "Бронко (мин)",
                "fields": [
                    {
                        "key": "result5",
                        "label": "Результат актуальный",
                        "type": "time",
                        "required": True,
                    },
                    {
                        "key": "force5",
                        "label": "Относил. Сила",
                        "type": "time",
                        "required": True,
                    },
                    {
                        "label": "Норма World Class",
                        "type": "info5",
                        "value": "Нап. < 5:00, Защ. < 4:40",
                    },
                ],
            },
        ],
    },
    {
        "key": "sport",
        "label": "Спортивная подготовка",
        "type": "select",
        "options": ["Спортивная подготовка", "Личная подготовка"],
        "required": True,
    },
]


TEAM_SURVEY_MAIN_DATA: dict[SportsTypes, list] = {
    SportsTypes.RUGBY: DEFAULT_MAIN_DATA,
    SportsTypes.FOOTBALL: DEFAULT_MAIN_DATA,
    SportsTypes.BASKETBALL: DEFAULT_MAIN_DATA,
    SportsTypes.TENNIS: DEFAULT_MAIN_DATA,
}

TEAM_SURVEY_ADD_DATA: dict[SportsTypes, list] = {
    SportsTypes.RUGBY: DEFAULT_ADD_DATA,
    SportsTypes.FOOTBALL: DEFAULT_ADD_DATA,
    SportsTypes.BASKETBALL: DEFAULT_ADD_DATA,
    SportsTypes.TENNIS: DEFAULT_ADD_DATA,
}
