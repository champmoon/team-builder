from ..base_docs import Docs

get_workouts_pool: Docs = {
    "summary": "Получение всех программ тренировок тренера",
    "description": """
    ```
    Query Params:
        id - ID программы тренировок.(uuid|null)(default=null)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Полученные программы тренировки",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                            "name": "string",
                            "estimatedTime": 3635,
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
                        },
                        {
                            "id": "633d5492-d5ca-4928-ab14-654b7d88445d",
                            "name": "14234234",
                            "estimatedTime": 0,
                            "createdAt": "2023-11-26T12:46:05.658562",
                            "exercises": [],
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
            "description": "Программа тренировок не найдена(id).",
            "content": {"application/json": {"example": {"detail": "workout_pool"}}},
        },
    },
}


create_workout_pool: Docs = {
    "summary": "Создание программы тренировок",
    "description": """
    ```
    Request Body:
        name - имя тренировки.
               (string)

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

    P.S
        1. exercises это массив упражнений.
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

        Н̶а̶ ̶ч̶т̶о̶ ̶я̶ ̶т̶р̶а̶ч̶у̶ ̶с̶в̶о̶ю̶ ̶ж̶и̶з̶н̶ь̶?
    """,
    "responses": {
        201: {
            "description": "Новая программы тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
    },
}


delete_workout_pool: Docs = {
    "summary": "Удаление программы тренировок",
    "description": """
    ```
    Query Params:
        id - ID программы тренировок.(uuid)
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        204: {
            "description": "УСпешно удалено",
            "content": {
                "application/json": {"example": {}},
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
            "description": "Программа тренировок не найдена(id).",
            "content": {"application/json": {"example": {"detail": "workout_pool"}}},
        },
    },
}


update_workout_pool: Docs = {
    "summary": "Обновление программы тренировок",
    "description": """
    ```
    Query Params:
        id - ID программы тренировок.(uuid)

    Request Body:
        name - имя тренировки.
               (string|null)

        estimatedTime - приблизительное время выполенения тренировки.
                        (float|null)

        exercises - массив упражнений.
                    (array[exercises]|null)


    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Обновленая программы тренировки",
            "content": {
                "application/json": {
                    "example": {
                        "id": "30cf6ca9-f944-448a-a479-0926eb75e24e",
                        "name": "string",
                        "estimatedTime": 3635,
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
            "description": "Программа тренировок не найдена(id).",
            "content": {"application/json": {"example": {"detail": "workout_pool"}}},
        },
    },
}
