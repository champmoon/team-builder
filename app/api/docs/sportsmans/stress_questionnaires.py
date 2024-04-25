from ..base_docs import Docs

get_active_stress_questionnaires: Docs = {
    "summary": "Получение всех активных нагрузочных опросников",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        То есть запрос возвращает все нагрузочные опросники,
        которые можно заполнить.
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
                        "rating": 0,
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
            "description": "Пользователь не является спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}


get_all_stress_questionnaires: Docs = {
    "summary": "Получение всех пройденных нагрузочных опросников",
    "description": """
    ```
    Query params:
        start_date - дата начала.(date)(default=null)

        end_date - дата окончания.(date)(default=null)

    Auth:
        Этот запрос доступен только спортсменом.

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
                        "rating": 0,
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
            "description": "Пользователь не является спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}


get_stress_questionnaire: Docs = {
    "summary": "Получение нагрузочного опросника",
    "description": """
    ```
    Path params:
        id - ID нагрузочного опросника.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        То есть запрос возвращает любой нагрузочный опросник,
        который когда было был назначен спортсмену после тренировоки,
        заполненный или нет, прошедший или активный в данный момент.
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
                        "rating": 0,
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


get_stress_questionnaire_by_workout_id: Docs = {
    "summary": "Получение нагрузочного опросника по тренировке",
    "description": """
    ```
    Path params:
        workout_id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        То есть запрос возвращает любой нагрузочный опросник,
        который когда было был назначен спортсмену после тренировоки,
        заполненный или нет, прошедший или активный в данный момент.
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
                        "rating": 0,
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


fill_stress_questionnaire: Docs = {
    "summary": "Заполнение нагрузочного опросника",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        Этот запрос позволяет заполнить активный опросник,
        их можно найти в списке всех активных опросников.
        Заполнить опросник можно только один раз. Далее,
        опросник становится прошедшим и всё блять.
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
                        "rating": 10,
                        "text": "AHYENNO",
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
        409: {
            "description": "Опросник не является активным.",
            "content": {
                "application/json": {"example": {"detail": "stress_questionnaire"}}
            },
        },
    },
}
