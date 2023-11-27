from ..base_docs import Docs

get_exercises_types: Docs = {
    "summary": "Получение всех типов упражнений",
    "description": """
    ```
    Auth:
        Этот запрос доступен всем типам пользователей.

    P.S
        Поле isBasic показывает, это упражнение basic или support.
        Это важно при создании тренировок, там и описано различие.
    """,
    "responses": {
        200: {
            "description": "Получение типов упражнений",
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
