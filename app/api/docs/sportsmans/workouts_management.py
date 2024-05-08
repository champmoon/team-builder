from ..base_docs import Docs

start_workout: Docs = {
    "summary": "Начать тренировку",
    "description": """
    ```
    Path params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.
    """,
    "responses": {
        200: {
            "description": "Полученная тренировка",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "status": {"status": 2, "description": "В процессе"},
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не в статусе Запланированна.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


complete_workout: Docs = {
    "summary": "Закончить тренировку",
    "description": """
    ```
    Path params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.
    """,
    "responses": {
        200: {
            "description": "Полученная тренировка",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
                        "status": {"status": 3, "description": "Завершена"},
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не в статусе В прогрессу.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}


cancel_workout: Docs = {
    "summary": "Отменить тренировку",
    "description": """
    ```
    Path params:
        id - ID тренировки.(uuid)

    Auth:
        Этот запрос доступен только спортсменом.
    """,
    "responses": {
        200: {
            "description": "Полученная тренировка",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
                        "status": {"status": 5, "description": "Отменена"},
                        "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
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
            "description": "Тренировка не найдена.",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
        409: {
            "description": "Тренировка не в статусе В прогрессу.",
            "content": {"application/json": {"example": {"detail": "workout_status"}}},
        },
    },
}
