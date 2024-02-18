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

    P.S
        В ответе статуса 200 параметр teamId всегда
        присылвает ID команды, из которой он вышел.
        Можно сказать, что это данные до выполнения этого запроса,
        так как после этого запроса параметр teamId станет равным null
    """,
    "responses": {
        200: {
            "description": "Получена команда спортсмена",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
            "content": {"application/json": {"example": {"detail": "Team not found"}}},
        },
        500: {
            "description": "Ошибка сервера: команды не существует",
            "content": {"application/json": {"example": {"detail": "Team must exist"}}},
        },
    },
}
