from app.consts.sports_types import SportsTypes

DEFAULT_MAIN_DATA = [
    {
        "key": "gender",
        "label": "Пол",
        "type": "select",
        "options": ["Мужской", "Женский"],
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
        "label": "Физическая подготовка",
        "type": "table",
        "rowsLength": 6,
        "rows": [
            "Норматив",
            "Жим лежа(кг)",
            "Приседания(кг)",
            "10м(с)",
            "30м(с)",
            "Бронко",
        ],
        "columnsLength": 4,
        "columns": ["Норматив", "Результат актуальный", "Относил. Сила", "Норма"],
        "cells": [
            {
                "key": "press__current",
                "rowIndex": 1,
                "columnIndex": 1,
                "type": "number",
                "required": True,
            },
            {
                "key": "press__relative",
                "rowIndex": 1,
                "columnIndex": 2,
                "type": "number",
                "required": True,
            },
            {
                "rowIndex": 1,
                "columnIndex": 3,
                "type": "info",
                "placeholder": ">1.4",
            },
            {
                "key": "squat__current",
                "rowIndex": 2,
                "columnIndex": 1,
                "type": "number",
                "required": True,
            },
            {
                "key": "squat__relative",
                "rowIndex": 2,
                "columnIndex": 2,
                "type": "number",
                "required": True,
            },
            {
                "rowIndex": 2,
                "columnIndex": 3,
                "type": "info",
                "placeholder": ">1.7",
            },
            {
                "key": "ten__current",
                "rowIndex": 3,
                "columnIndex": 1,
                "type": "number",
                "required": True,
            },
            {
                "key": "ten__relative",
                "rowIndex": 3,
                "columnIndex": 2,
                "type": "number",
                "required": True,
            },
            {
                "rowIndex": 3,
                "columnIndex": 3,
                "type": "info",
                "placeholder": "Нап(Forwards). <1,70 Защит(Backs) <1,60",
            },
            {
                "key": "thirty__current",
                "rowIndex": 4,
                "columnIndex": 1,
                "type": "number",
                "required": True,
            },
            {
                "key": "thirty__relative",
                "rowIndex": 4,
                "columnIndex": 2,
                "type": "number",
                "required": True,
            },
            {
                "rowIndex": 4,
                "columnIndex": 3,
                "type": "info",
                "placeholder": "Нап(Forwards). <4,20 Защит(Backs) <4,00",
            },
            {
                "key": "bron__current",
                "rowIndex": 5,
                "columnIndex": 1,
                "type": "time",
                "required": True,
            },
            {
                "key": "bron__relative",
                "rowIndex": 5,
                "columnIndex": 2,
                "type": "time",
                "required": True,
            },
            {
                "rowIndex": 5,
                "columnIndex": 3,
                "type": "info",
                "placeholder": "Нап(Forwards). <5:00 Защит(Backs) <4:40",
            },
        ],
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
