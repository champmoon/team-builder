from ..base_docs import Docs

get_workouts_statuses: Docs = {
    "summary": "Получение всех статусов тренировок",
    "description": """
    ```
    Auth:
        Этот запрос доступен всем типам пользователей.

    """,
    "responses": {
        200: {
            "description": "Получение статусов тренивок",
            "content": {
                "application/json": {
                    "example": [
                        {"status": 1, "description": "Запланирована"},
                        {"status": 2, "description": "В процессе"},
                        {"status": 3, "description": "Завершена"},
                        {"status": 4, "description": "Активна"},
                        {"status": 5, "description": "Отменена"},
                        {"status": 6, "description": "Пропущена"},
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
