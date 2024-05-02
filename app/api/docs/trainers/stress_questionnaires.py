from ..base_docs import Docs

get_all_stress_questionnaires_by_sportsman: Docs = {
    "summary": "Получение всех нагрузочных опросников спортсмена",
    "description": """
    ```
    Query Params:
        email - email спортсмена(str).

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Полученные опросники",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "workoutId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "rating": 9,
                        "text": "PIZDATO",
                        "createdAt": "2024-04-04T16:27:21.929Z",
                    }],
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
        404: {
            "description": "Спортсмен не найден.",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
    },
}


get_all_stress_questionnaires_by_workout: Docs = {
    "summary": "Получение всех нагрузочных опросников тренировки",
    "description": """
    ```
    Query Params:
        id - ID тренировки(str).

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Полученные опросники",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "workoutId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "rating": 9,
                        "text": "PIZDATO",
                        "createdAt": "2024-04-04T16:27:21.929Z",
                    }],
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
        404: {
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
    },
}


get_stress_questionnaire: Docs = {
    "summary": "Получение нагрузочного опросника",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Полученный опросник",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "workoutId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "rating": 9,
                        "text": "PIZDATO",
                        "createdAt": "2024-04-04T16:27:21.929Z",
                    },
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
        404: {
            "description": "Опросник не найден.",
            "content": {
                "application/json": {"example": {"detail": "stress_questionnaire"}}
            },
        },
    },
}
