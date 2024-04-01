from ..base_docs import Docs

get_workouts_for_team: Docs = {
    "summary": "Получение всех тренировок команды тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2023-11-26T15:59:16.358000",
                            "createdAt": "2023-11-26T12:00:53.249510",
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
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
                        {
                            "id": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
                            "workoutType": "Командная",
                            "teamId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
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
    },
}


create_workout_for_team: Docs = {
    "summary": "Создание тренировки для команды",
    "description": """
    ```
    Request Body:
        workoutPoolId - ID тренировки из пула.
               (uuid)

        date - время начала тренировки.
               (datetime)

        restTime - время отдыха после тренировки(в сек).
                   (int)(>0)

        stressQuestionnaireTime - время для нагрузочного опросника(в сек).
                                  (int)(>0)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "restTime": 123,
                        "stressQuestionnaireTime": 321,
                        "status": {"status": 1, "description": "Запланирована"},
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
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
            "description": "Тренировчкая программа не найдена",
            "content": {"application/json": {"example": {"detail": "workout_pool"}}},
        },
        409: {
            "description": "Пустая команды",
            "content": {"application/json": {"example": {"detail": "team"}}},
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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


get_workouts_for_group: Docs = {
    "summary": "Получение всех тренировок группы тренера",
    "description": """
    ```
    Query params:
        id - ID группы.(uuid)

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2023-11-26T15:59:16.358000",
                            "createdAt": "2023-11-26T12:00:53.249510",
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
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
                            "workoutType": "Групповая",
                            "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "id": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
                            "workoutType": "Групповая",
                            "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Группа не найдена.",
            "content": {"application/json": {"example": {"detail": "group"}}},
        },
    },
}


create_workout_for_group: Docs = {
    "summary": "Создание тренировки для группы",
    "description": """
    ```
    Request Body:
        workoutPoolId - ID тренировки из пула.
               (uuid)

        groupId - ID группы.(uuid)

        date - время начала тренировки.
               (datetime)

        restTime - время отдыха после тренировки(в сек).
                   (int)(>0)

        stressQuestionnaireTime - время для нагрузочного опросника(в сек).
                                  (int)(>0)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "restTime": 123,
                        "stressQuestionnaireTime": 321,
                        "status": {"status": 1, "description": "Запланирована"},
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
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
                        "workoutType": "Групповая",
                        "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Что-то не найдено",
            "content": {
                "application/json": {
                    "examples": {
                        "workout_pool": {
                            "summary": "Тренировочная программа не найдена",
                            "description": "Тренировочная программа не найдена",
                            "value": {"detail": "workout_pool"},
                        },
                        "group": {
                            "summary": "Группа не найдена",
                            "description": "Группа не найдена",
                            "value": {"detail": "group"},
                        },
                    }
                }
            },
        },
        409: {
            "description": "Пустая группа",
            "content": {"application/json": {"example": {"detail": "group"}}},
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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


get_workouts_for_sportsman: Docs = {
    "summary": "Получение всех тренировок спортсмена тренера",
    "description": """
    ```
    Query params:
        email - email спортсмена.(str)

    Auth:
        Этот запрос доступен только тренерам.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2023-11-26T15:59:16.358000",
                            "createdAt": "2023-11-26T12:00:53.249510",
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
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
                            "workoutType": "Групповая",
                            "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "id": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
                            "workoutType": "Командная",
                            "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "id": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "restTime": 123,
                            "stressQuestionnaireTime": 321,
                            "workoutType": "Индивидуальная",
                            "sportsmanId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Спортсмен не найден.",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
    },
}


create_workout_for_sportsman: Docs = {
    "summary": "Создание тренировки для спортсмена",
    "description": """
    ```
    Request Body:
        workoutPoolId - ID тренировки из пула.
               (uuid)

        sportsmanEmail - email спортсмена.(str)

        date - время начала тренировки.
               (datetime)

        restTime - время отдыха после тренировки(в сек).
                   (int)(>0)

        stressQuestionnaireTime - время для нагрузочного опросника(в сек).
                                  (int)(>0)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "restTime": 123,
                        "stressQuestionnaireTime": 321,
                        "status": {"status": 1, "description": "Запланирована"},
                        "date": "2023-11-26T15:59:16.358000",
                        "createdAt": "2023-11-26T12:00:53.249510",
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
                        "workoutType": "Индивидуальная",
                        "sportsmanId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Что-то не найдено",
            "content": {
                "application/json": {
                    "examples": {
                        "workout_pool": {
                            "summary": "Тренировочная программа не найдена",
                            "description": "Тренировочная программа не найдена",
                            "value": {"detail": "workout_pool"},
                        },
                        "group": {
                            "summary": "Спортсмен не найден",
                            "description": "Спортсмен не найден",
                            "value": {"detail": "sportsman"},
                        },
                    }
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
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

