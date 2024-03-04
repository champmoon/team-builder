from ..base_docs import Docs

get_profile: Docs = {
    "summary": "Получение профиля тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен профиль тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "string",
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


update_profile: Docs = {
    "summary": "Обновление профиля тренера",
    "description": """
    ```
    Request Body:
        name - имя тренера.
               (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен обновлённый профиль тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "new",
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
        422: {
            "description": "Ошибка валидации, `name` невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_type",
                                "loc": ["body", "name"],
                                "msg": "Input should be a valid string",
                                "input": 1,
                            }
                        ]
                    }
                }
            },
        },
    },
}
