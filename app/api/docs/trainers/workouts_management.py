from ..base_docs import Docs

start_workout: Docs = {
    "summary": "Старт тренировки",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не Активна, Запланированна или В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


start_workout_for_sportsmans: Docs = {
    "summary": "Старт тренировки для выбранных спортсменов",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Request Body:
        sportsmansEmails - список email спортсменов.(list[str])

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                    },
                },
            },
        },
        400: {
            "description": "Переданным спортсменов нельзя поменять статус тренировки.",
            "content": {"application/json": {"example": {"detail": "sportsmans"}}},
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
        409: {
            "description": "Тренировка не Активна, Запланированна или В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


complete_workout: Docs = {
    "summary": "Завершение тренировки",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


complete_workout_for_sportsmans: Docs = {
    "summary": "Завершение тренировки для выбранных спортсменов",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Request Body:
        sportsmansEmails - список email спортсменов.(list[str])

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                    },
                },
            },
        },
        400: {
            "description": "Переданным спортсменов нельзя поменять статус тренировки.",
            "content": {"application/json": {"example": {"detail": "sportsmans"}}},
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
        409: {
            "description": "Тренировка не В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


cancel_workout: Docs = {
    "summary": "Отмена тренировки",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


cancel_workout_for_sportsmans: Docs = {
    "summary": "Отмена тренировки для выбранных спортсменов",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Request Body:
        sportsmansEmails - список email спортсменов.(list[str])

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Измененная тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
                        "restTime": 123,
                        "price": 321,
                        "exercises": [
                            {
                                "type": {
                                    "type": 4,
                                    "description": "Отжимания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 1,
                            },
                            {
                                "type": {
                                    "type": 1,
                                    "description": "Отдых",
                                    "isBasic": False,
                                },
                                "time": 123,
                                "order": 2,
                            },
                            {
                                "type": {
                                    "type": 5,
                                    "description": "Подтягивания",
                                    "isBasic": True,
                                },
                                "reps": 3,
                                "sets": 3,
                                "rest": 3,
                                "order": 3,
                            },
                            {
                                "type": {
                                    "type": 6,
                                    "description": "Приседания",
                                    "isBasic": True,
                                },
                                "reps": 2,
                                "sets": 233,
                                "rest": 13,
                                "order": 4,
                            },
                        ],
                        "workoutType": "Командная",
                        "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                    },
                },
            },
        },
        400: {
            "description": "Переданным спортсменов нельзя поменять статус тренировки.",
            "content": {"application/json": {"example": {"detail": "sportsmans"}}},
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
        409: {
            "description": "Тренировка не В процессе.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


get_workout_statuses: Docs = {
    "summary": "Получение статусов тренировки у спортсменов",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid)

    Request Body:
        sportsmansEmails - список email спортсменов.
            (list[str]|null)(deafult=null)

    Auth:
        Этот запрос доступен только тренерам.

    P.S:
        Если не передать список email спортсменов
        вернутся статусы всех спортсменов данной тренировки.
    """,
    "responses": {
        200: {
            "description": "Полученные статусы",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "workoutId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "string",
                            "firstName": "string",
                            "middleName": "string",
                            "lastName": "string",
                        },
                        {
                            "sportsmanId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "workoutId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "string",
                            "firstName": "string",
                            "middleName": "string",
                            "lastName": "string",
                        },
                    ]
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
