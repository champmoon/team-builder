from ..base_docs import Docs

get_self_team: Docs = {
    "summary": "Получение команды тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportsmans": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "first@sportsman.com",
                            "name": "first",
                            "sportType": "rugby",
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


add_sportsman_to_team: Docs = {
    "summary": "Добавление спортсмена в команду",
    "description": """
    ```
    Request Body:
        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                        ],
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
        404: {
            "description": "Добавляемый спортсмен не найден.",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
        409: {
            "description": (
                "Добавляемый спортсмен уже состоит в какой-то команде(в этой же или"
                " другой)."
            ),
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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


adds_sportsmans_to_team: Docs = {
    "summary": "Добавление спортсменов в команду",
    "description": """
    ```
    Request Body:
        sportsmansEmails - почты спортсмена.
                           (array[string])

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Этот запрос позволяет сразу добавить несколько спортсменов.
        Однако тут игнорируются ошибки по каждому спортсмену.
        Добавляются только "валидные" спортсмены.

    """,
    "responses": {
        200: {
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "third@sportsman.com",
                                "name": "third",
                            },
                        ],
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
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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


kick_sportsman_off_team: Docs = {
    "summary": "Удаление спортсмена из команду",
    "description": """
    ```
    Request Body:
        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая команда тренера",
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
        404: {
            "description": "Удаляемый спортсмен не найден.",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
        409: {
            "description": "Удаляемый спортсмен не состоит в этой команде",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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


kicks_sportsmans_off_team: Docs = {
    "summary": "Удаление спортсменов из команду",
    "description": """
    ```
    Request Body:
        sportsmansEmails - почты спортсмена.
                           (array[string])

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Этот запрос позволяет сразу удалять несколько спортсменов.
        Однако тут игнорируются ошибки по каждому спортсмену.
        Удаляются только "валидные" спортсмены.

    """,
    "responses": {
        200: {
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
                        "sportsmans": [],
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
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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
