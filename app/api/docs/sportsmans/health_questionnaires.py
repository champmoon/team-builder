from ..base_docs import Docs

get_active_health_questionnaire: Docs = {
    "summary": "Получение активного опросника по здоровью",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменом.
    """,
    "responses": {
        200: {
            "description": "Полученный опросник",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
            "description": "Опросника по здороью нет.",
            "content": {
                "application/json": {"example": {"detail": "health_questionnaire"}}
            },
        },
    },
}


get_all_health_questionnaires: Docs = {
    "summary": "Получение всех пройденных опросников по здоровью",
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
                    "example": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "rating": 10,
                            "text": "AHUENNO DAVAI ESHE",
                            "createdAt": "2024-04-04T16:27:21.929Z",
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "rating": 1,
                            "text": "GOVNO KAKOE TO",
                            "createdAt": "2024-04-04T16:27:21.929Z",
                        },
                    ],
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


get_health_questionnaire: Docs = {
    "summary": "Получение опросника по здоровью",
    "description": """
    ```
    Path params:
        id - ID опросника по здоровью.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        То есть запрос возвращает любой опросник по здоровью,
        прошедший или активный
    """,
    "responses": {
        200: {
            "description": "Полученный опросник",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "rating": 7,
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
                "application/json": {"example": {"detail": "health_questionnaire"}}
            },
        },
    },
}


fill_health_questionnaire: Docs = {
    "summary": "Заполнение опросника по здоровью",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменом.

    P.S:
        Этот запрос позволяет заполнить активный опросник.
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
                "application/json": {"example": {"detail": "health_questionnaire"}}
            },
        },
    },
}
