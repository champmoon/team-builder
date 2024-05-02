from ..base_docs import Docs

get_survey: Docs = {
    "summary": "Получение анкеты спортсмена",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Получена анкета спортсмена",
            "content": {
                "application/json": {
                    "example": {
                        "answers": [{"key": "string", "value": "string"}],
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
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}

get_survey_update_flag: Docs = {
    "summary": "Получение флага возможномти обновления анкеты спортсмена",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Спортсмен может обновить анкету",
            "content": {
                "application/json": {"example": {}},
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        423: {
            "description": "Спортсмен не может обновить анкету",
            "content": {
                "application/json": {"example": {"detail": "sportsman_survey"}}
            },
        },
    },
}


fill_survey: Docs = {
    "summary": "Обновление анкеты спортсмена",
    "description": """
    ```
    Request Body:
        answers - список объектов key value(list[objects])

    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Спортсмен успешно обновил анкету",
            "content": {
                "application/json": {
                    "example": {
                        "answers": [{"key": "string", "value": "string"}],
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
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        423: {
            "description": "Спортсмен не может обновить анкету",
            "content": {
                "application/json": {"example": {"detail": "sportsman_survey"}}
            },
        },
    },
}
