from ..base_docs import Docs

create_exercise_type: Docs = {
    "summary": "Создать новый тип упражнения",
    "description": """
    ```
    Request Body:
        type - тип упражнения.(int)
        description - описание типа упражнения.(string)
        isBasic - тип упражнения basic или support.(bool)

    Auth:
        Этот запрос доступен только тренерам.

    P.S
        Поле isBasic показывает, это упражнение basic или support.
        Это важно при создании тренировок, там и описано различие.
    """,
    "responses": {
        201: {
            "description": "Новый тип упражнения",
            "content": {
                "application/json": {
                    "example": {
                        "type": 16,
                        "description": "Воздушные приседания",
                        "isBasic": True,
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        409: {
            "description": "Этот тип упражнения уже существует.",
            "content": {"application/json": {"example": {"detail": "exercises_type"}}},
        },
    },
}


update_exercise_type: Docs = {
    "summary": "Обновить тип упражнения",
    "description": """
    ```
    Request Body:
        type - тип упражнения.(int)
        description - описание типа упражнения.(string)
        isBasic - тип упражнения basic или support.(bool)

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "ОБновленный тип упражнения",
            "content": {
                "application/json": {
                    "example": {
                        "type": 16,
                        "description": "Воздушные приседания",
                        "isBasic": True,
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        404: {
            "description": "Тип упражнения не найден.",
            "content": {"application/json": {"example": {"detail": "exercises_type"}}},
        },
    },
}


delete_exercise_type: Docs = {
    "summary": "Удалить тип упражнения",
    "description": """
    ```
    Query Params:
        type - тип упражнения.(int)

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Удалённый тип упражнения",
            "content": {
                "application/json": {
                    "example": {
                        "type": 16,
                        "description": "Воздушные приседания",
                        "isBasic": True,
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        404: {
            "description": "Тип упражнения не найден.",
            "content": {"application/json": {"example": {"detail": "exercises_type"}}},
        },
    },
}

reset_exercises_types: Docs = {
    "summary": "Сброс типов упражнений до дефолтных",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Дефолтные типы упражнения",
            "content": {
                "application/json": {
                    "example": [
                        {"type": 1, "description": "Отдых", "isBasic": False},
                        {"type": 2, "description": "Разминка", "isBasic": False},
                        {"type": 3, "description": "Заминка", "isBasic": False},
                        {"type": 4, "description": "Отжимания", "isBasic": True},
                        {"type": 5, "description": "Подтягивания", "isBasic": True},
                        {"type": 6, "description": "Приседания", "isBasic": True},
                        {"type": 7, "description": "Бёрпи", "isBasic": True},
                    ]
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
    },
}
