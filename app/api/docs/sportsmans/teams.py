from ..base_docs import Docs

get_self_team: Docs = {
    "summary": "Получение команды спортсмена",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Получена команда спортсмена",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
                        "sportsmans": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "first@sportsman.com",
                            "name": "first",
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


out_off_team: Docs = {
    "summary": "Выход из команды",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменам.

    """,
    "responses": {
        200: {
            "description": "Спортсмен",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
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
            "description": "Спортсмен не состоит в команде",
            "content": {"application/json": {"example": {"detail": "team"}}},
        },
    },
}


join_team: Docs = {
    "summary": "Вступить в команду",
    "description": """
    ```
    Request Body:
        confirmToken - токен.
                       (UUID)

    Auth:
        Этот запрос доступен только спортсменам.

    P.S
        Это токен из ссылки приглашение в команду.

    """,
    "responses": {
        200: {
            "description": "Спортсмен",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
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
        409: {
            "description": "Спортсмен уже в команде",
            "content": {"application/json": {"example": {}}},
        },
        410: {
            "description": "Токен протух",
            "content": {"application/json": {"example": {}}},
        },
        422: {
            "description": "Ошибка валидации",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
    },
}
