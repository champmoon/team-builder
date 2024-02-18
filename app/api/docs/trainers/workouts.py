from ..base_docs import Docs

create_workout_for_sportsman: Docs = {
    "summary": "Создание тренировки для спорстмена",
    "description": """
    ```
    Request Body:
        name - имя тренировки.
               (string)

        date - время начала тренировки.
               (datetime)(P.S)

        estimatedTime - приблизительное время выполенения тренировки.
                        (float)

        exercises - массив упражнений.
                    (array[exercises])(P.S)

            type - тип упраженения.
                   (integer)(only=[basic | support])

            reps - кол-во повторений.
                   (integer)(only=[basic])

            sets - кол-во подходов.
                   (integer)(only=[basic])

            rest - время отдыха между подходами.
                   (float | null)(only=[basic])(P.S)

            time - время выполнение всего управженения.
                   (float)(only=[support])

        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.

    P.S
        1. date присылается без таймзоны

        2. exercises это массив упражнений.
           Упраженения делятся на 2 типа: basic и support.
           a) Basic упраженения - это основные упражнения типо приседаний
                                                           и подтягиваний.
              Для таких упраженений всегда указываются type, reps, sets, rest?.

              Важно! Если при создании указывается поле sets равным 1,
                     то поле rest не должно присылаться.

           b) Support упражнения - это вспомогательные упражнения типо отдых
                                                                  и разминка
              Для таких упражнения всегда указываюся type и time.

        3. На выходе для упражнений всегда будет присылаться поле order,
           которое показывает порядок упражнений в тренировке.
           Порядок будет проставляться в зависимости от порядка присылаемого на сервер.

        4. Также добавится поле created_at, время создание тренировки на сервере.
           Оно никак не связано с полем date.

        5. Также будет присылаться статус тренировки.
           Статусы тренировки могут быть:
               1. Запланирована
               2. В процессе
               3. Завершена.
            Т.е в ответе будет типо такого
                "status": {
                    "status": 1,
                    "description": "Запланирована"
                }

            Важно! Статусы тренировок у тренера, который её создал,
                   и спорсменов будут разные.

        Н̶а̶ ̶ч̶т̶о̶ ̶я̶ ̶т̶р̶а̶ч̶у̶ ̶с̶в̶о̶ю̶ ̶ж̶и̶з̶н̶ь̶?̶

    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
            "description": "Cпортсмен не найден.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sportsman with email {sportsmanEmail} not found"
                    }
                }
            },
        },
        409: {
            "description": "Cпортсмен не состоит в команде тренера",
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Sportsman with email {sportsmanEmail} not be on a team"
                        )
                    }
                }
            },
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


create_workout_for_group: Docs = {
    "summary": "Создание тренировки для группы",
    "description": """
    ```
    Request Body:
        name - имя тренировки.
               (string)

        date - время начала тренировки.
               (datetime)(P.S)

        estimatedTime - приблизительное время выполенения тренировки.
                        (float)

        exercises - массив упражнений.
                    (array[exercises])(P.S)

            type - тип упраженения.
                   (integer)(only=[basic | support])

            reps - кол-во повторений.
                   (integer)(only=[basic])

            sets - кол-во подходов.
                   (integer)(only=[basic])

            rest - время отдыха между подходами.
                   (float | null)(only=[basic])(P.S)

            time - время выполнение всего управженения.
                   (float)(only=[support])

        groupId - id группы.
                  (uuid)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Дополнительно про Request Body можно найти
            в доке запроса "create_workout_for_sportsman"

    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
            "description": "Группы не найдена.",
            "content": {
                "application/json": {
                    "example": {"detail": "Group with id {groupId} not found"}
                }
            },
        },
        409: {
            "description": "Пустая группы",
            "content": {
                "application/json": {
                    "example": {"detail": "The group must not be empty"}
                }
            },
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


create_workout_for_team: Docs = {
    "summary": "Создание тренировки для команды",
    "description": """
    ```
    Request Body:
        name - имя тренировки.
               (string)

        date - время начала тренировки.
               (datetime)(P.S)

        estimatedTime - приблизительное время выполенения тренировки.
                        (float)

        exercises - массив упражнений.
                    (array[exercises])(P.S)

            type - тип упраженения.
                   (integer)(only=[basic | support])

            reps - кол-во повторений.
                   (integer)(only=[basic])

            sets - кол-во подходов.
                   (integer)(only=[basic])

            rest - время отдыха между подходами.
                   (float | null)(only=[basic])(P.S)

            time - время выполнение всего управженения.
                   (float)(only=[support])

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Дополнительно про Request Body можно найти
            в доке запроса "create_workout_for_sportsman"

    """,
    "responses": {
        201: {
            "description": "Тренировка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
        409: {
            "description": "Пустая команды",
            "content": {
                "application/json": {
                    "example": {"detail": "The team must not be empty"}
                }
            },
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


get_workouts: Docs = {
    "summary": "Получение всех тренировок, которые назначил тренер",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
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
                            "workoutType": 1,
                            "sportsmanId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "wertertertertertertert",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 3,
                            "teamId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 2,
                            "groupId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
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


get_workout: Docs = {
    "summary": "Получение тренировки, которую назначил тренер, по id.",
    "description": """
    ```
    Path Params:
        id - id тренировки.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Полученная тренировка",
            "content": {
                "application/json": {
                    "example": {
                        "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
                        "workoutType": 2,
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
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": (
                "Не найдена тренировка или тренировка есть,"
                "но она создана другим тренером"
            ),
            "content": {
                "application/json": {"example": {"detail": "Workout not found"}}
            },
        },
    },
}


get_workouts_for_sportsman: Docs = {
    "summary": "Получение всех тренировок спортсмена",
    "description": """
    ```
    Path Params:
        email - email тренировки.
                (string)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
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
                            "workoutType": 1,
                            "sportsmanId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "wertertertertertertert",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 3,
                            "teamId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 2,
                            "groupId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
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
            "description": "Спортсмен не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} not found"}
                }
            },
        },
        409: {
            "description": "Спортсмен не состоит в команде",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sportsman with email {email} not be on a team"
                    }
                }
            },
        },
    },
}


get_workouts_for_group: Docs = {
    "summary": "Получение всех тренировок группы",
    "description": """
    ```
    Path Params:
        id - id группы.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
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
                            "workoutType": 2,
                            "groupId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 2,
                            "groupId": "e32cb56e-28a7-4abe-89de-b4b4d5b76e9b",
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
            "description": "Группа не найдена или это группа другого тренера",
            "content": {
                "application/json": {
                    "example": {"detail": "Group with id {id} not found"}
                }
            },
        },
    },
}


get_workouts_for_team: Docs = {
    "summary": "Получение всех тренировок команды тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
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
                            "workoutType": 3,
                            "teamId": "f69103e0-faf5-48a9-b3b6-197be69965ba",
                        },
                        {
                            "workoutId": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "status": {"status": 1, "description": "Запланирована"},
                            "date": "2024-11-26T12:45:39.760000",
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
                            "workoutType": 3,
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


delete_workout: Docs = {
    "summary": "Удаление тренировки по id.",
    "description": """
    ```
    Path Params:
        id - id тренировки.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Поля, присылаемые с ответе, такие же, как и при создании тренирок.
        Однако добавляются и новое поле workoutType - тип тренировки.

        Если workoutType - 1, то:
            1. Это тренировка - индивидуальная, то есть только для одного спортсмена.
            2. Также присылается поле sportsmanId - id спорстсмена.

        Если workoutType - 2, то:
            1. Это тренировки - групповой, то есть для группы спортсменов.
            2. Также присылается поле groupId - id группы.

        Если workoutType - 3, то:
            1. Это тренировки - командная, то есть для команды спортсменов.
            2. Также присылается поле teamId - id команды.

    """,
    "responses": {
        200: {
            "description": "Удаленная тренировка",
            "content": {
                "application/json": {
                    "example": {
                        "workoutId": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
                        "workoutType": 2,
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
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": (
                "Не найдена тренировка или тренировка есть,"
                "но она создана другим тренером"
            ),
            "content": {
                "application/json": {"example": {"detail": "Workout not found"}}
            },
        },
    },
}
