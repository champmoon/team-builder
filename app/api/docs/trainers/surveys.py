from ..base_docs import Docs

get_survey: Docs = {
    "summary": "Получение анкеты тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    P.S:
        Пример статус кода 200 - http://158.160.118.208/files/example_survey.pdf
    """,
    "responses": {
        200: {
            "description": "Получена анкета",
            "content": {
                "application/json": {
                    "example": {
                        "mainFields": [
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
                        ],
                        "addFields": [{
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
                            "columns": [
                                "Норматив",
                                "Результат актуальный",
                                "Относил. Сила",
                                "Норма",
                            ],
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
                                    "placeholder": (
                                        "Нап(Forwards). <1,70 Защит(Backs) <1,60"
                                    ),
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
                                    "placeholder": (
                                        "Нап(Forwards). <4,20 Защит(Backs) <4,00"
                                    ),
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
                                    "placeholder": (
                                        "Нап(Forwards). <5:00 Защит(Backs) <4:40"
                                    ),
                                },
                            ],
                        }],
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}


update_survey: Docs = {
    "summary": "Обновление доп. полей анкеты тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Получена анкета",
            "content": {
                "application/json": {
                    "example": {
                        "mainFields": [
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
                        ],
                        "addFields": [{
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
                            "columns": [
                                "Норматив",
                                "Результат актуальный",
                                "Относил. Сила",
                                "Норма",
                            ],
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
                                    "placeholder": (
                                        "Нап(Forwards). <1,70 Защит(Backs) <1,60"
                                    ),
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
                                    "placeholder": (
                                        "Нап(Forwards). <4,20 Защит(Backs) <4,00"
                                    ),
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
                                    "placeholder": (
                                        "Нап(Forwards). <5:00 Защит(Backs) <4:40"
                                    ),
                                },
                            ],
                        }],
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}

get_sportsman_survey: Docs = {
    "summary": "Получение анкеты спортсмена",
    "description": """
    ```
    Path Params:
        email - Email спортсмена(str).

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Анкета спортсмена.",
            "content": {
                "application/json": {
                    "example": {
                        "answers": [{"key": "123", "value": "312"}],
                        "survey": {
                            "mainFields": [
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
                            ],
                            "addFields": [{
                                "key": "1",
                                "label": "1",
                                "type": "text",
                                "required": True,
                            }],
                        },
                    }
                }
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Спортсмен не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} not found"}
                }
            },
        },
        409: {
            "description": "Спортсмен не в этой команде.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sportsman with email {email} not be on a team"
                    }
                }
            },
        },
    },
}


set_update_sportsman_survey: Docs = {
    "summary": "Дать возможность анкеты спортсмена",
    "description": """
    ```
    Path Params:
        email - Email спортсмена(str).

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Спортмен может теперь обновить анкету.",
            "content": {"application/json": {"example": {}}},
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Спортсмен не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} not found"}
                }
            },
        },
        409: {
            "description": "Спортсмен не в этой команде.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sportsman with email {email} not be on a team"
                    }
                }
            },
        },
    },
}

set_update_team_survey: Docs = {
    "summary": "Дать возможность анкеты всей команде",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Команда спортсменов может теперь обновить анкету.",
            "content": {"application/json": {"example": {}}},
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}
